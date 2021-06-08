package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"sync"
	"time"
)

const N int = 3
const itération int = 131405

//somme de deux vecteurs
func vsomme(vect1 [3]float64, vect2 [3]float64) [3]float64 {
	var v [3]float64
	for i := 0; i < 3; i++ {
		v[i] = vect1[i] + vect2[i]
	}
	return v
}

//multiplication d'un vecteur par un réel
func vmul(p1 [3]float64, m float64) [3]float64 {
	var v [3]float64
	for i := 0; i < 3; i++ {
		v[i] = m * p1[i]
	}
	return v
}

// différence entre deux vecteurs
func vdif(p1 [3]float64, p2 [3]float64) [3]float64 {
	var v [3]float64
	for i := 0; i < 3; i++ {
		v[i] = p1[i] - p2[i]
	}
	return v
}

//norme d'un vecteur
func norme(p1 [3]float64) float64 {
	var n float64
	for i := 0; i < 3; i++ {
		n += p1[i] * p1[i]
	}
	return (math.Sqrt(n))
}

func calculAcc(i int, positions [N][3]float64, M [N]float64, canal chan [4]float64, wg *sync.WaitGroup) {
	var A [3]float64 = [3]float64{0, 0, 0}
	var g float64 = 6.6743e-11
	for j := 0; j < N; j++ {
		if j != i {
			p1, p2 := positions[j], positions[i]
			var p1p2 [3]float64 = vdif(p1, p2)
			var facteur float64 = g * M[j] / math.Pow(norme(p1p2), 3)
			A = vsomme(A, vmul(p1p2, facteur))
		}

	}
	canal <- [4]float64{float64(i), A[0], A[1], A[2]}
	wg.Done()
}

func calculAllAcc(positions [N][3]float64, M [N]float64) [N][3]float64 {
	canal := make(chan [4]float64, N)
	var ACC [N][3]float64
	var wg sync.WaitGroup

	for i := 0; i < len(M); i++ {
		wg.Add(1)
		go calculAcc(i, positions, M, canal, &wg)

	}
	wg.Wait()
	for i := 0; i < N; i++ {
		A := <-canal
		n := int(A[0])
		ACC[n] = [3]float64{A[1], A[2], A[3]}
	}
	return ACC
}

func calculNextPosition(position [3]float64, vitesse [3]float64, Acc [3]float64, h float64, corps float64, c chan [7]float64, wg2 *sync.WaitGroup) {
	hcarre := h * h / 2
	V := vsomme(vitesse, vmul(Acc, h))
	P := vsomme(position, vsomme(vmul(vitesse, h), vmul(Acc, hcarre)))
	c <- [7]float64{corps, P[0], P[1], P[2], V[0], V[1], V[2]}
	wg2.Done()
}

func calculAllNextPosi(PN [N][3]float64, VN [N][3]float64, AN [N][3]float64, h float64) ([N][3]float64, [N][3]float64) {
	canal2 := make(chan [7]float64, N)
	var V, P [N][3]float64
	var wg2 sync.WaitGroup
	wg2.Add(N)
	for i := 0; i < N; i++ {

		var position, vitesse, acc [3]float64
		position, vitesse, acc = PN[i], VN[i], AN[i]

		go calculNextPosition(position, vitesse, acc, h, float64(i), canal2, &wg2)

	}

	wg2.Wait()
	for i := 0; i < N; i++ {
		elem := <-canal2
		//fmt.Println(elem)
		n := int(elem[0])
		V[n] = [3]float64{elem[4], elem[5], elem[6]}
		P[n] = [3]float64{elem[1], elem[2], elem[3]}
	}
	return P, V
}

type retour struct {
	Soleil      [itération][3]float64
	Terre1      [itération][3]float64
	Terre2      [itération][3]float64
	Temps       time.Duration
	nombreCoeur int
}

func main() {
	now := time.Now()

	var positions [N][3]float64
	var vitesses [N][3]float64
	var m [N]float64

	positions[0] = [3]float64{0, 0, 0}
	positions[1] = [3]float64{149597870700., 0, 0}
	positions[2] = [3]float64{0, 0, 149597870700.}

	vitesses[0] = [3]float64{0, 0, 0}
	vitesses[1] = [3]float64{0, 30000, 0}
	vitesses[2] = [3]float64{0, -30000, 0}

	m = [3]float64{1.989e30, 5.972e24, 5.972e24}

	//for i := 0; i < N; i++ {
	//	positions[i] = [3]float64{150 * rand.Float64(), 3800. * rand.Float64(), 3800. * rand.Float64()}
	//	vitesses[i] = [3]float64{29970. + 100*rand.Float64(), 32444. + 85*rand.Float64(), 32444. + 85*rand.Float64()}
	//	m[i] = 23.3e24 + rand.Float64()
	//}

	var Terre1, Terre2, Soleil [itération][3]float64

	for i := 0; i < itération; i++ {
		Soleil[i] = positions[0]
		Terre1[i] = positions[1]
		Terre2[i] = positions[2]
		Acc := calculAllAcc(positions, m)

		positions, vitesses = calculAllNextPosi(positions, vitesses, Acc, 240)

	}
	temps := time.Now().Sub(now)
	DTS := norme(vdif(Soleil[itération-1], Terre1[itération-1]))
	fmt.Println("DTS = ", DTS)
	DTS2 := norme(vdif(Soleil[itération-1], Terre2[itération-1]))
	fmt.Println("DTS2 = ", DTS2)
	Positions, err := json.Marshal(retour{Soleil, Terre1, Terre2, temps, 4})
	if err != nil {
		fmt.Println("Error:", err)
	}

	_ = ioutil.WriteFile("3corps.json", Positions, 0644)
	//fmt.Println(time.Now().Sub(now))
	//fmt.Println(Trajectoires[itération-1][0])
	//fmt.Println(Trajectoires[itération-1][1])
	//fmt.Println(Trajectoires[itération-1][2])
}

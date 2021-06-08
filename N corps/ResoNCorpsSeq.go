package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

const N = 9 // nombre de corps

//somme de deux vecteurs
func vsomme(p1 [3]float64, p2 [3]float64) [3]float64 {
	var v [3]float64
	for i := 0; i < 3; i++ {
		v[i] = p1[i] + p2[i]
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

// acceleration d'un corps induite par la force exercée par un autre
func force2(m1 float64, p1 [3]float64, m2 float64, p2 [3]float64) [3]float64 {
	var G float64 = 6.67e-11
	var p1p2 [3]float64 = vdif(p1, p2)
	var facteur float64 = G * m2 / math.Pow(norme(p1p2), 2)
	return vmul(p1p2, facteur)
}

// force exercée par N-1 corps sur le j-ème corps
func forceN(j int, m [N]float64, pos [N][3]float64) [3]float64 {

	var force [3]float64
	for i := 0; i < len(m); i++ {
		if i != j {
			force = vsomme(force, force2(m[i], pos[i], m[j], pos[j]))
		}

	}
	return force
}

// position et vitesse suivante d'un corps utlisant la méthode de verlet
func posSuivant(m [N]float64, pos [N][3]float64, vit [N][3]float64, h float64) [2][N][3]float64 {
	var h2sur2 float64 = h * h / 2
	var r [2][N][3]float64
	var pos2 [N][3]float64
	var acc [N][3]float64

	for i := 0; i < len(m); i++ {
		acc[i] = forceN(i, m, pos)
		pos2[i] = vsomme(pos[i], vsomme(vmul(vit[i], h), vmul(acc[i], h2sur2)))
	}
	r[0] = pos2
	r[1] = acc
	return r
}

// état suivant des N corps du système
func etatSuivant(m [N]float64, pos [N][3]float64, vit [N][3]float64, h float64) [2][N][3]float64 {
	var posip1 [N][3]float64 = posSuivant(m, pos, vit, h)[0]
	var acci [N][3]float64 = posSuivant(m, pos, vit, h)[1]
	var accip1 [N][3]float64
	var vit2 [N][3]float64

	for i := 0; i < len(m); i++ {
		accip1[i] = vmul(forceN(i, m, posip1), 1/m[i])
		vit2[i] = vsomme(vit[i], vmul(vsomme(acci[i], accip1[i]), h/2))
	}
	var result [2][N][3]float64
	result[0] = posip1
	result[1] = vit2
	return result
}

// simulation totale de la résolutation
func simulation(h float64, n int, pos0 [N][3]float64, vit0 [N][3]float64, masse [N]float64) [100000][N][3]float64 {

	var pos [N][3]float64

	var position [100000][N][3]float64
	position[0] = pos0
	var vit [N][3]float64
	pos = pos0
	vit = vit0

	for i := 0; i < n; i++ {
		pos = etatSuivant(masse, pos, vit, h)[0]
		vit = etatSuivant(masse, pos, vit, h)[1]

		position[i] = pos
	}
	return position

}

func organisationResult(result [1000][3][3]float64) [3][1000][3]float64 {
	var pos1 [1000][3]float64
	var pos2 [1000][3]float64
	var pos3 [1000][3]float64
	var res [3][1000][3]float64
	for i := 0; i < 1000; i++ {
		pos1[i] = result[i][0]
		pos2[i] = result[i][1]
		pos3[i] = result[i][2]
	}
	res[0] = pos1
	res[1] = pos2
	res[2] = pos3
	return res

}

type retour struct {
	corps1 [1000][3]float64
	corps2 [1000][3]float64
	corps3 [1000][3]float64
}

func main() {

	var now = time.Now()
	var pos [N][3]float64
	var vit [N][3]float64
	var m [N]float64
	for i := 0; i < N; i++ {
		pos[i] = [3]float64{12.4 + rand.Float64(), 23.8 + rand.Float64()}
		vit[i] = [3]float64{2.8 + rand.Float64(), 3.4 + rand.Float64()}
		m[i] = 236.6 + rand.Float64()
	}

	var r [100000][N][3]float64
	r = simulation(0.2, 100000, pos, vit, m)
	fmt.Println(r[0][0][1])

	fmt.Println(time.Now().Sub(now))
}

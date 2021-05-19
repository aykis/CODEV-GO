package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"sync"
	//"time"
)

func calculAcc(i int, X [3]float64, Y [3]float64, M [3]float64, canal chan [2]float64, wg *sync.WaitGroup) {
	var axi float64 = 0
	var ayi float64 = 0
	var g float64 = 6.6743e-11
	for j := 0; j < len(X); j++ {
		if j != i {
			r, theta := cmplx.Polar(complex(X[j]-X[i], Y[j]-Y[i]))
			f := M[j] * g / (r * r)
			axi += f * math.Cos(theta)
			ayi += f * math.Sin(theta)
		}

	}
	canal <- [2]float64{axi, ayi}
	wg.Done()
}

func calculAllAcc(X [3]float64, Y [3]float64, M [3]float64) ([3]float64, [3]float64) {
	canal := make(chan [2]float64)
	var AXI [3]float64
	var AYI [3]float64
	var wg sync.WaitGroup

	for i := 0; i < len(X); i++ {
		wg.Add(1)
		go calculAcc(i, X, Y, M, canal, &wg)
		A := <-canal
		AYI[i] = A[1]
		AXI[i] = A[0]

	}
	wg.Wait()
	return AXI, AYI
}

func calculNextPosition(xn float64, yn float64, vxn float64, vyn float64, axi float64, ayi float64, h float64, c chan [4]float64, wg2 *sync.WaitGroup) {
	vx := vxn + axi*h
	vy := vyn + ayi*h
	x := xn + (vxn+vx)/2*h
	y := yn + (vyn+vy)/2*h
	c <- [4]float64{x, y, vx, vy}
	wg2.Done()
}

func calculAllNextPosi(XN [3]float64, YN [3]float64, VXN [3]float64, VYN [3]float64, AXI [3]float64, AYI [3]float64, h float64) ([3]float64, [3]float64, [3]float64, [3]float64) {
	canal2 := make(chan [4]float64)
	var VX, VY, X, Y [3]float64
	var wg2 sync.WaitGroup

	for i := 0; i < len(XN); i++ {
		var xn, yn, vxn, vyn, axi, ayi float64
		xn, yn, vxn, vyn, axi, ayi = XN[i], YN[i], VXN[i], VYN[i], AXI[i], AYI[i]
		wg2.Add(1)
		go calculNextPosition(xn, yn, vxn, vyn, axi, ayi, h, canal2, &wg2)
		result := <-canal2
		X[i] = result[0]
		Y[i] = result[1]
		VX[i] = result[2]
		VY[i] = result[3]
	}
	wg2.Wait()
	return X, Y, VX, VY
}

func main() {
	X := [3]float64{0., 149597870700., 0.}
	Y := [3]float64{0., 0., 227939200.}
	M := [3]float64{1.989e30, 5.972e24, 6.39e23}
	VX := [3]float64{0, 0, -24130}
	VY := [3]float64{0, 29700, 0}
	const itération int = 534707
	var TrajX, TrajY [itération][3]float64

	for i := 0; i < itération; i++ {
		TrajX[i] = X
		TrajY[i] = Y
		Axi, Ayi := calculAllAcc(X, Y, M)

		X, Y, VX, VY = calculAllNextPosi(X, Y, VX, VY, Axi, Ayi, 60)

	}

	for i := 0; i < 105; i++ {
		fmt.Println("Position", 5000*i)
		fmt.Println(TrajX[5000*i], TrajY[5000*i])
	}
	DistTerreSoleil, angle := cmplx.Polar(complex(TrajX[itération-1][1]-TrajX[itération-1][0], TrajY[itération-1][1]-TrajY[itération-1][0]))
	DistMarsSoleil, angle2 := cmplx.Polar(complex(TrajX[itération-1][2]-TrajX[itération-1][0], TrajY[itération-1][2]-TrajY[itération-1][0]))
	fmt.Println("DTS=", DistTerreSoleil, angle, "DMS =", DistMarsSoleil, angle2)
	fmt.Println("dernière position de la Terre", TrajX[itération-1][1]-TrajX[itération-1][0], TrajY[itération-1][1]-TrajY[itération-1][0])
	fmt.Println("vitesse de la terre : ", VX[1], VY[1])
}

package main

import (
	"fmt"
	"math"
	"math/cmplx"
)

func fft(a []complex128) []complex128 {
	n := len(a)
	b := true
	if n == 1 {
		return (a)
	} else {
		even := make([]complex128, n/2)
		odd := make([]complex128, n-n/2)
		for i, elt := range a {
			if b {
				even[i/2] = elt
			} else {
				odd[(i-1)/2] = elt
			}
			b = !b
		}
		pair := fft(even)
		impair := fft(odd)
		rep := make([]complex128, n)
		for i := 0; i < (n / 2); i++ {
			t := impair[i] * cmplx.Rect(1, -2*math.Pi*(float64(i)/float64(n)))
			rep[i] = pair[i] + t
			rep[i+n/2] = pair[i] - t
		}
		return (rep)
	}

}

func main() {
	a := []complex128{0.00000000e+00, 3.94355855e-01, 7.24792787e-01, 9.37752132e-01,
		9.98716507e-01, 8.97804540e-01, 6.51372483e-01, 2.99363123e-01,
		-1.01168322e-01, -4.85301963e-01, -7.90775737e-01, -9.68077119e-01,
		-9.88468324e-01, -8.48644257e-01, -5.71268215e-01, -2.01298520e-01,
		2.01298520e-01, 5.71268215e-01, 8.48644257e-01, 9.88468324e-01,
		9.68077119e-01, 7.90775737e-01, 4.85301963e-01, 1.01168322e-01,
		-2.99363123e-01, -6.51372483e-01, -8.97804540e-01, -9.98716507e-01,
		-9.37752132e-01, -7.24792787e-01, -3.94355855e-01, -4.89858720e-16}

	test := fft(a)
	fmt.Println(test)
}

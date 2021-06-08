package main

import (
	"encoding/json"
	"fmt"
	"math"
	"math/cmplx"
	"os"
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
func abs_fft(a []complex128) []float64 {
	a_fft := fft(a)
	n := len(a_fft)
	rep := make([]float64, n)
	for i := 0; i < n; i++ {
		rep[i] = cmplx.Abs(a_fft[i])
	}
	return (rep)
}
func fft_freq(n int, dt float64) []float64 {
	rep := make([]float64, n)
	if n%2 == 0 {
		for i := 0; i < n/2; i++ {
			rep[i] = (float64(i) / (float64(n) * dt))
			rep[n/2-i] = (float64(i-n/2) / (float64(n) * dt))
		}
	} else {
		for i := 0; i < (n-1)/2; i++ {
			rep[i] = (float64(i) / (float64(n) * dt))
			rep[(n-1)/2-i+1] = (float64(i-(n-1)/2) / (float64(n) * dt))
		}
		rep[(n-1)/2] = (float64((n-1)/2) / (float64(n) * dt))
	}
	return (rep)
}

func main() {
	jsonFile, err := os.Open(os.Args[2])
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()
	a := []complex128{0.0, 0.1}
	test := abs_fft(a)
	result, err := json.Marshal(test)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(result)

}

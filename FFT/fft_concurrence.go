package main

import (
	"fmt"
	"math"
	"math/cmplx"
	"sync"
	"time"
)

func fft(a []complex128) []complex128 {
	n := len(a)
	b := true
	if n == 1 {
		return (a)
	} else {
		// on sépare la séquence en pair et impair
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
		//on fait l'appel récursif
		pair := fft(even)
		impair := fft(odd)
		rep := make([]complex128, n)
		for i := 0; i < (n / 2); i++ {
			t := impair[i] * cmplx.Rect(1, -2*math.Pi*(float64(i)/float64(n))) // on multiplie la séquence impair par w**n
			// on ré-agence les parties paires et impaires
			rep[i] = pair[i] + t
			rep[i+n/2] = pair[i] - t
		}
		return (rep)
	}

}

// Création des structures
type Job struct {
	id       int
	last     bool
	dec_last int
	length   int
	dec      int
	tab      []complex128
}
type Result struct {
	id      int
	tab_fft []complex128
}

// création des channels
var jobs = make(chan Job, 100)
var results = make(chan Result, 100)

//exécution de la fft/ traitement des Jobs par un worker
func worker(wg *sync.WaitGroup) {
	for job := range jobs {
		if job.id == 0 {
			output := Result{job.id, fft(job.tab)[:job.length-job.dec]}
			results <- output
		} else if job.last {
			output := Result{job.id, fft(job.tab)[job.dec_last:]}
			results <- output
		} else {
			output := Result{job.id, fft(job.tab)[job.dec : job.length-job.dec]}
			results <- output
		}

	}
	wg.Done()
}

// création de la worker pool
func createWorkerPool(noOfWorkers int) {
	var wg sync.WaitGroup
	for i := 0; i < noOfWorkers; i++ {
		wg.Add(1)
		go worker(&wg)
	}
	wg.Wait()
	close(results)
}

// séparation du signal en séquences plus petites
func allocate(length int, dec int, a []complex128) {
	n := len(a)
	count := 0
	for i := 0; i < n-length; {
		if i == 0 {
			tab := a[:length]
			job := Job{count, false, 0, length, dec / 2, tab}
			jobs <- job
			i += length - dec
			count += 1
		} else {
			tab := a[i : i+length]
			job := Job{count, false, 0, length, dec / 2, tab}
			jobs <- job
			i += length - dec
			count += 1
		}

		if i >= n-length {
			tab_last := a[n-length:]
			job_last := Job{count, true, i - n + length, length, dec / 2, tab_last}
			jobs <- job_last
			count += 1
		}
	}

	close(jobs)
}

// regroupement des séquences en un tableau
func result(done chan bool, rep [][]complex128) {
	for result := range results {
		rep[result.id] = result.tab_fft
	}
	done <- true
}

func creer_tab(n int) []complex128 {
	val := make([]complex128, n)
	b := true
	for i := 0; i < n; i++ {
		if b {
			val[i] = complex128(8.978045e-01 / 2.02104)
		} else {
			val[i] = complex128(7.8045e-01 / 1.02496)
		}
	}
	return (val)
}
func main() {
	startTime := time.Now()
	length := 8
	dec := 2
	a := []complex128{0.00000000e+00, 3.94355855e-01, 7.24792787e-01, 9.37752132e-01,
		9.98716507e-01, 8.97804540e-01, 6.51372483e-01, 2.99363123e-01,
		-1.01168322e-01, -4.85301963e-01, -7.90775737e-01, -9.68077119e-01,
		-9.88468324e-01, -8.48644257e-01, -5.71268215e-01, -2.01298520e-01,
		2.01298520e-01, 5.71268215e-01, 8.48644257e-01, 9.88468324e-01,
		9.68077119e-01, 7.90775737e-01, 4.85301963e-01, 1.01168322e-01,
		-2.99363123e-01, -6.51372483e-01, -8.97804540e-01, -9.98716507e-01,
		-9.37752132e-01, -7.24792787e-01, -3.94355855e-01, -4.89858720e-16}

	//fmt.Println(a)

	go allocate(length, dec, a)
	done := make(chan bool)
	rep := make([][]complex128, len(a))
	go result(done, rep)
	noOfWorkers := 10
	createWorkerPool(noOfWorkers)
	<-done
	endTime := time.Now()
	diff := endTime.Sub(startTime)
	//mesure du temps d'exécution
	fmt.Println("total time taken ", diff.Seconds(), "seconds")

	//fmt.Println(rep)
	start := time.Now()
	fft(a)
	end := time.Now()
	//fmt.Println("test :", test)
	diffs := end.Sub(start)
	fmt.Println("total time taken no conc ", diffs.Seconds(), "seconds")

}

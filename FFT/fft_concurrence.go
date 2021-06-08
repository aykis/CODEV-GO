package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math"
	"math/cmplx"
	"os"
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
func abs_fft(a []complex128) []float64 {
	a_fft := fft(a)
	n := len(a_fft)
	rep := make([]float64, n)
	for i := 0; i < n; i++ {
		rep[i] = cmplx.Abs(a_fft[i])
	}
	return (rep)
}

// Création des structures
type Job struct {
	id       int
	last     bool
	dec_last int
	length   int
	dec      int
	tab      []complex128
	dt       float64
}
type Result struct {
	id      int
	tab_fft []float64
	freq    []float64
}

// création des channels
var jobs = make(chan Job, 100)
var results = make(chan Result, 100)

//exécution de la fft/ traitement des Jobs par un worker
func worker(wg *sync.WaitGroup) {
	for job := range jobs {
		if job.id == 0 {
			output := Result{job.id, abs_fft(job.tab)[:job.length-job.dec], fft_freq(job.length, job.dt)[:job.length-job.dec]}
			results <- output
		} else if job.last {
			output := Result{job.id, abs_fft(job.tab)[job.dec_last:], fft_freq(job.length, job.dt)[job.dec_last:]}
			results <- output
		} else {
			output := Result{job.id, abs_fft(job.tab)[job.dec : job.length-job.dec], fft_freq(job.length, job.dt)[job.dec : job.length-job.dec]}
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
func allocate(length int, dec int, a []complex128, dt float64) {
	n := len(a)
	count := 0
	for i := 0; i < n-length; {
		if i == 0 {
			tab := a[:length]
			job := Job{count, false, 0, length, dec / 2, tab, dt}
			jobs <- job
			i += length - dec
			count += 1
		} else {
			tab := a[i : i+length]
			job := Job{count, false, 0, length, dec / 2, tab, dt}
			jobs <- job
			i += length - dec
			count += 1
		}

		if i >= n-length {
			tab_last := a[n-length:]
			job_last := Job{count, true, i - n + length, length, dec / 2, tab_last, dt}
			jobs <- job_last
			count += 1
		}
	}

	close(jobs)
}

// regroupement des séquences en un tableau
func result(done chan bool, rep [][]float64, freq_rep [][]float64) {
	for result := range results {
		rep[result.id] = result.tab_fft
		freq_rep[result.id] = result.freq
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

type Retour struct {
	fft_abs   [][]float64
	frequence [][]float64
	temps     float64
	nbcoeurs  string
}
type Entree struct {
	Y   []float64
	pas float64
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
	// Open our jsonFile
	jsonFile, err := os.Open(os.Args[2])
	// if we os.Open returns an error then handle it
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened users.json")
	// defer the closing of our jsonFile so that we can parse it later on
	defer jsonFile.Close()

	byteValue, _ := ioutil.ReadAll(jsonFile)

	var entree Entree
	json.Unmarshal([]byte(byteValue), &entree)

	startTime := time.Now()
	length := 256
	dec := 2
	dt := entree.pas
	b := entree.Y
	a := make([]complex128, len(b))
	for i := 0; i < len(b); i++ {
		a[i] = complex(b[i], 0)
	}
	//a := []complex128{0.00000000e+00, 3.94355855e-01, 7.24792787e-01, 9.37752132e-01,
	//	9.98716507e-01, 8.97804540e-01, 6.51372483e-01, 2.99363123e-01,
	//	-1.01168322e-01, -4.85301963e-01, -7.90775737e-01, -9.68077119e-01,
	//	-9.88468324e-01, -8.48644257e-01, -5.71268215e-01, -2.01298520e-01,
	//	2.01298520e-01, 5.71268215e-01, 8.48644257e-01, 9.88468324e-01,
	//	9.68077119e-01, 7.90775737e-01, 4.85301963e-01, 1.01168322e-01,
	//	-2.99363123e-01, -6.51372483e-01, -8.97804540e-01, -9.98716507e-01,
	//	-9.37752132e-01, -7.24792787e-01, -3.94355855e-01, -4.89858720e-16}

	//fmt.Println(a)

	go allocate(length, dec, a, dt)
	done := make(chan bool)
	rep := make([][]float64, len(a))
	freq := make([][]float64, len(a))
	go result(done, rep, freq)
	noOfWorkers := 100
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
	retour := Retour{rep, freq, diff.Seconds(), "Nombre de goroutines : 100"}
	valeur, er := json.Marshal(retour)
	if er != nil {
		fmt.Println(er)
	}
	erre := ioutil.WriteFile(os.Args[2], valeur, 0777)
	// handle this error
	if erre != nil {
		// print it out
		fmt.Println(erre)
	}

}

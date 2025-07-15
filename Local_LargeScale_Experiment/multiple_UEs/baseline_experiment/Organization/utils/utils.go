package utils

import (
	"math"
	"net/url"
)

func CheckUrl(str string) bool {
	u, err := url.Parse(str)
	if err != nil || u.Scheme == "" || u.Host == "" {
		return false
	} else {
		return true
	}
}

func CheckPort(port int) bool {
	if port >= 1024 && port <= 65535 {
		return true
	} else {
		return false
	}
}

func SliceAverage(arr []float64) float64 {

	if len(arr) == 0 {
		return 0
	}

	count := 0.0
	for i := 0; i < len(arr); i++ {
		count += arr[i]
	}
	return count / float64(len(arr))
}

func SliceMax(arr []float64) float64 {
	if len(arr) == 0 {
		return 0
	}

	max := 0.0

	for i := 0; i < len(arr); i++ {
		if arr[i] > max {
			max = arr[i]
		}
	}
	return max
}

func SliceMin(arr []float64) float64 {
	if len(arr) == 0 {
		return 0
	}

	min := math.MaxFloat64

	for i := 0; i < len(arr); i++ {
		if arr[i] < min {
			min = arr[i]
		}
	}
	return min
}

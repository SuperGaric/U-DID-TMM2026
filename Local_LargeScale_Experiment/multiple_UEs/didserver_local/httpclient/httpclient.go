package httpclient

import (
	"bytes"
	"io/ioutil"
	"net/http"
)

// SendGET sends an HTTP GET request to the provided URL and returns the response body.
func SendGET(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return string(body), nil
}

// SendPOST sends an HTTP POST request with provided data to the provided URL and returns the response body.
func SendPOST(url string, contentType string, data []byte) (string, error) {
	resp, err := http.Post(url, contentType, bytes.NewBuffer(data))
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return string(body), nil
}

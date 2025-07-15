package client

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"mime/multipart"
	"net/http"
)

func sendHttpPost(dperurl string, buf bytes.Buffer, writer *multipart.Writer) string {
	// 创建一个http请求
	req, err := http.NewRequest("POST", dperurl, &buf)
	if err != nil {
		panic(err)
	}
	// 设置请求头Content-Type为multipart/form-data
	if writer != nil {
		req.Header.Set("Content-Type", writer.FormDataContentType())
	}

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// 读取响应内容
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return ""
	}
	// 打印响应内容

	return string(body)
}

func sendHttpGet(dperurl string) string {
	var buf bytes.Buffer
	// 创建一个http请求
	req, err := http.NewRequest("GET", dperurl, &buf)
	if err != nil {
		panic(err)
	}

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// 读取响应内容
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return ""
	}

	// 打印响应内容
	//fmt.Printf("now: %s ---- %s\n", time.Now().Format("2006-01-02 15:04:05"), string(body))
	return string(body)
}

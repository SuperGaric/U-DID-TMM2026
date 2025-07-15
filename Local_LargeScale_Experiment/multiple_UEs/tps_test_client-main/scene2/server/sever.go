// server.go
package main

import (
	"bytes"
	"encoding/base64"
	"dper/common"
	"dper/crypto"
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"regexp"
	"time"
)

func main() {
	http.HandleFunc("/signature", handleSignature)
	fmt.Println("服务端在 :8080 端口监听签名请求")

	go func() {
		time.Sleep(2 * time.Second)

		message := "Hello, this is a test message."
		fmt.Println("启动时自动发送消息给客户端:", message)

		signature, did, err := requestClientSignature(message)
		if err != nil {
			log.Printf("启动时发送消息失败: %v", err)
			return
		}

		address, err := getAddress(did)
		if err != nil {
			log.Printf("获取地址失败: %v", err)
			return
		}
		newaddress := extractHexAddress(address)
		fmt.Println("提取的地址:", newaddress)

		ok, err := verifySignature(message, signature, newaddress)
		if err != nil {
			log.Printf("验证签名失败: %v", err)
			return
		}

		if ok {
			log.Println("签名验证成功")
			go sendResultToClient("验证成功")
		} else {
			log.Println("签名验证失败")
		}
	}()

	log.Fatal(http.ListenAndServe(":8080", nil))
}

func handleSignature(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "仅支持POST方法", http.StatusMethodNotAllowed)
		return
	}
	err := r.ParseMultipartForm(10 << 20)
	if err != nil {
		http.Error(w, "解析表单失败", http.StatusInternalServerError)
		log.Printf("解析表单失败: %v", err)
		return
	}

	did := r.FormValue("DID")
	signatureBase64 := r.FormValue("signature")
	if did == "" || signatureBase64 == "" {
		http.Error(w, "缺少必要字段", http.StatusBadRequest)
		return
	}

	signature, err := base64.StdEncoding.DecodeString(signatureBase64)
	if err != nil {
		http.Error(w, "签名Base64解码失败", http.StatusBadRequest)
		log.Printf("签名解码失败: %v", err)
		return
	}

	address, err := getAddress(did)
	if err != nil {
		http.Error(w, "获取地址失败", http.StatusInternalServerError)
		log.Printf("获取地址失败: %v", err)
		return
	}
	newaddress := extractHexAddress(address)

	ok, err := verifySignature("Hello, this is a test message.", signature, newaddress)
	if err != nil {
		http.Error(w, "验证签名失败", http.StatusInternalServerError)
		return
	}

	if ok {
		w.Write([]byte("签名验证成功"))
		go sendResultToClient("验证成功")
	} else {
		http.Error(w, "签名验证失败", http.StatusUnauthorized)
	}
}

func requestClientSignature(message string) ([]byte, string, error) {
	clientURL := "http://127.0.0.1:8081/receive"

	payload := &bytes.Buffer{}
	writer := multipart.NewWriter(payload)
	writer.WriteField("message", message)
	writer.Close()

	req, err := http.NewRequest("POST", clientURL, payload)
	if err != nil {
		return nil, "", err
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, "", err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, "", fmt.Errorf("客户端响应错误: %s", resp.Status)
	}

	body, _ := io.ReadAll(resp.Body)
	fields := bytes.SplitN(body, []byte("|"), 2)
	if len(fields) != 2 {
		return nil, "", fmt.Errorf("响应格式错误")
	}

	signatureBase64 := string(fields[0])
	did := string(fields[1])
	signature, err := base64.StdEncoding.DecodeString(signatureBase64)
	if err != nil {
		return nil, "", fmt.Errorf("签名Base64解码失败: %w", err)
	}

	return signature, did, nil
}

func getAddress(did string) (string, error) {
	url := "http://127.0.0.1:8001/dper/getaddress"
	payload := &bytes.Buffer{}
	writer := multipart.NewWriter(payload)
	writer.WriteField("DID", did)
	writer.Close()

	req, err := http.NewRequest("POST", url, payload)
	if err != nil {
		return "", err
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func extractHexAddress(address string) string {
	re := regexp.MustCompile(`[a-fA-F0-9]{40}`)
	return re.FindString(address)
}

func verifySignature(message string, signature []byte, hexAddr string) (bool, error) {
	msg := common.BytesToHash([]byte(message))
	addr := common.HexToAddress(hexAddr)
	return crypto.SignatureValid(addr, signature, msg)
}

func sendResultToClient(result string) {
	clientURL := "http://127.0.0.1:8081/result"
	payload := &bytes.Buffer{}
	writer := multipart.NewWriter(payload)
	writer.WriteField("result", result)
	writer.Close()

	req, err := http.NewRequest("POST", clientURL, payload)
	if err != nil {
		log.Printf("创建请求失败: %v", err)
		return
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Printf("发送验证结果失败: %v", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		log.Println("验证结果成功发送给客户端")
	} else {
		log.Printf("客户端响应状态码: %v", resp.Status)
	}
}

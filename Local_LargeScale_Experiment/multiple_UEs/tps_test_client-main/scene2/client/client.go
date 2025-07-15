// client.go
package main

import (
	"bytes"
	"dper/accounts"
	"dper/common"
	"dper/crypto/keys"
	"encoding/base64"
	"fmt"
	"log"
	"mime/multipart"
	"net/http"
)

func main() {
	http.HandleFunc("/receive", handleReceive)
	http.HandleFunc("/result", handleResult)

	fmt.Println("客户端在 :8081 端口监听接收消息请求")
	log.Fatal(http.ListenAndServe(":8081", nil))
}

func handleReceive(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "仅支持POST方法", http.StatusMethodNotAllowed)
		return
	}

	r.ParseMultipartForm(10 << 20)
	message := r.FormValue("message")
	if message == "" {
		http.Error(w, "缺少message字段", http.StatusBadRequest)
		return
	}
	fmt.Println("收到消息:", message)

	keyStore := keys.NewKeyStorePlain("../../100keys/keystore")
	manager := accounts.NewManager(keyStore)
	accounts, _ := manager.Accounts()
	if len(accounts) == 0 {
		http.Error(w, "未找到账户", http.StatusInternalServerError)
		return
	}

	account := accounts[0]
	manager.Unlock(account.Address, "")
	hash := common.BytesToHash([]byte(message))
	signature, err := manager.SignHash(account, hash)
	if err != nil {
		http.Error(w, "签名失败", http.StatusInternalServerError)
		return
	}

	signatureBase64 := base64.StdEncoding.EncodeToString(signature)
	did := "DID:000000"

	// 同步响应签名和DID，格式：<signature>|<did>
	response := fmt.Sprintf("%s|%s", signatureBase64, did)
	w.Write([]byte(response))

	// 同时发POST到服务端（也可省略，只靠服务端拉取）
	go postSignature(signatureBase64, did)
}

func postSignature(signatureBase64, did string) {
	var buffer bytes.Buffer
	writer := multipart.NewWriter(&buffer)
	writer.WriteField("signature", signatureBase64)
	writer.WriteField("DID", did)
	writer.Close()

	req, _ := http.NewRequest("POST", "http://127.0.0.1:8080/signature", &buffer)
	req.Header.Set("Content-Type", writer.FormDataContentType())

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Printf("发送签名失败: %v", err)
		return
	}
	defer resp.Body.Close()

	log.Printf("签名已发送，服务端响应: %s", resp.Status)
}

func handleResult(w http.ResponseWriter, r *http.Request) {
	r.ParseMultipartForm(10 << 20)
	result := r.FormValue("result")
	fmt.Println("服务端返回验证结果:", result)
	w.WriteHeader(http.StatusOK)
}

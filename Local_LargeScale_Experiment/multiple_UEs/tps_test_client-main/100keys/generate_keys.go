package main

import (
	"bytes"
	"dper/accounts" // 请根据实际路径修改
	"dper/crypto/keys"
	"fmt"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net/http"
	"time"
)

func main() {
	// 初始化 KeyStore
	keyStoreDir := "./keystore" // 请根据实际路径修改
	keyStore := keys.NewKeyStorePlain(keyStoreDir)

	// 创建 Manager 实例
	manager := accounts.NewManager(keyStore)

	// 生成 10 个账户
	accounts := generateAccounts(manager, 1, "")

	// 打印并发送生成的账户地址
	for i, account := range accounts {
		address := account.Address.Hex()
		did := fmt.Sprintf("DID:%06d", i) // 生成递增的 DID
		fmt.Printf("DID: %s, Address: %s\n", did, address)
		err := setdid(did, address)
		if err != nil {
			log.Printf("发送地址失败: %v", err)
		} else {
			fmt.Printf("成功发送地址: %s\n", address)
		}
		time.Sleep(100 * time.Millisecond) // 添加100毫秒的延迟
	}
}

func generateAccounts(manager *accounts.Manager, count int, auth string) []accounts.Account {
	var accounts []accounts.Account

	for i := 0; i < count; i++ {
		account, err := manager.NewAccount(auth)
		if err != nil {
			log.Fatalf("Failed to create account %d: %v", i, err)
		}
		accounts = append(accounts, *account)
	}

	return accounts
}

func setdid(did, address string) error {
	url := "http://127.0.0.1:8001/dper/setdidnew"
	method := "POST"

	payload := &bytes.Buffer{}
	writer := multipart.NewWriter(payload)
	err := writer.WriteField("DID", did)
	if err != nil {
		return fmt.Errorf("创建 DID 字段失败: %w", err)
	}
	err = writer.WriteField("Address", address)
	if err != nil {
		return fmt.Errorf("创建 address 字段失败: %w", err)
	}
	err = writer.Close()
	if err != nil {
		return fmt.Errorf("关闭 writer 失败: %w", err)
	}

	client := &http.Client{}
	req, err := http.NewRequest(method, url, payload)
	if err != nil {
		return fmt.Errorf("创建请求失败: %w", err)
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	res, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("发送请求失败: %w", err)
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		return fmt.Errorf("读取响应失败: %w", err)
	}
	fmt.Println(string(body))

	if res.StatusCode != http.StatusOK {
		return fmt.Errorf("服务器返回错误状态: %v", res.Status)
	}

	return nil
}

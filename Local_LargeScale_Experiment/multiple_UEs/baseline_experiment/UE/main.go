/*
三、核心流程
1. 初始化阶段（Initialization）

    用户生成身份：
        用户生成SSI（如ID_UI）及公私钥对（PK_UI, SK_UI）。
        向发行者申请可验证声明（如学历证明），发行者签名后返回加密的声明。

    网络运营商授权：
        用户提交声明和签名至运营商。
        运营商验证签名和声明有效性，授权用户接入网络。

2. 区块链共识（Consensus）

    交易生成：
        运营商将授权用户的(ID, PK)打包为交易，使用变色龙哈希生成交易哈希。
        交易结构：Tx = {数据块m, 哈希h}，其中h = ChameleonHash(m, r, s)。

    共识机制：
        采用PBFT（实用拜占庭容错）算法，网络运营商组成联盟链。
        交易通过共识后写入区块链，变色龙哈希确保后续可编辑性。

*/

package main

import (
	"UE/crypto"
	"bytes"
	"crypto/ecdsa"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"time"
)

const KEY_STORE_PATH = "./keystore"

var publicKeyHex_Org = "04BE4F1BA1BD5C59E85C2BB6B3FAF99FD161DF9845B0C4E6363F110FB27DB65A76CBF5759CCC447327702FB9D32E827ED01DF7B9D7F6583C8F52BE2421E9A40F2B"

type VerifiableCredential struct {
	Context           []string `json:"@context"`
	Type              []string `json:"type"`
	Issuer            string   `json:"issuer"`       // 发行者DID
	IssuanceDate      string   `json:"issuanceDate"` // 颁发日期
	CredentialSubject struct {
		ID      string `json:"id"`      // 用户DID
		IMSI    string `json:"IMSI"`    // 用户IMSI
		Carrier string `json:"carrier"` // 运营商
	} `json:"credentialSubject"`
	Proof struct {
		Type               string `json:"type"`               // 签名算法类型
		Created            string `json:"created"`            // 签名时间
		ProofPurpose       string `json:"proofPurpose"`       // 签名用途
		VerificationMethod string `json:"verificationMethod"` // 验证方法
		SignatureValue     string `json:"signatureValue"`     // 数字签名
	} `json:"proof"`
}

type DiDQuery struct {
	DID string `json:"IMSI"`
}

type didDocument struct {
	Id string
	Pk string
}

type sigResponse struct {
	Signature string `json:"signature"`
	Status    string `json:"status"`
}

// 发送message请求签名
// func sig_request(message string) string {
// 	response, err := httpclient.SendPOST("http://"+pathHttp+"/dper/signaturereturn", "application/json", []byte(message))
// 	if err != nil {
// 		fmt.Println("Error:", err)

// 	}
// 	fmt.Println("POST Response:", response)

// 	var respSignData sigResponse
// 	err = json.Unmarshal([]byte(response), &respSignData)
// 	if err != nil {
// 		panic(err)
// 	}
// 	sign := respSignData.Signature
// 	return sign
// }

// did生成

func document_generate(imsi string, privateKey *ecdsa.PrivateKey, address string) didDocument {
	var diddocument didDocument
	hash := sha256.Sum256([]byte(imsi))

	signature, _ := crypto.Sign(hash[:], privateKey)

	// 将哈希值转换为十六进制字符串
	signString := hex.EncodeToString(signature[:])

	diddocument.Id = "DID:IMSI:" + signString
	diddocument.Pk = address
	return diddocument
}

type TransTemp struct {
	// head
	TxID      string
	Sender    string
	Nonce     uint64
	Version   string
	LifeTime  uint8 // the max lagging versions after the current one
	Signature []byte

	//body
	Contract string
	Function string
	Args     []string // function argument
}

type AccountResponse struct {
	Code int `json:"code"`
	Data struct {
		Accounts []string `json:"accounts"`
	} `json:"data"`
	Msg string `json:"msg"`
}

var dq DiDQuery

func sendFormDataRequest2(url, address, key1Value string) {
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// Add fields to the form
	_ = writer.WriteField("account", address)
	_ = writer.WriteField("password", key1Value)
	_ = writer.Close()

	req, err := http.NewRequest("POST", url, body)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()

	// Read and print the response
	respBody, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("POST Response:", string(respBody))
}

func sendFormDataRequest3(url, key1, value1, key2, value2, key3, value3 string) {
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// Add fields to the form
	_ = writer.WriteField(key1, value1)
	_ = writer.WriteField(key2, value2) // Corrected here
	_ = writer.WriteField(key3, value3) // Corrected here
	_ = writer.Close()

	req, err := http.NewRequest("POST", url, body)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()

	// Read and print the response
	respBody, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("POST Response:", string(respBody))
}

func sendFormDataRequest4(url, key1, value1, key2, value2 string) {
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// Add fields to the form
	_ = writer.WriteField(key1, value1)
	_ = writer.WriteField(key2, value2) // Corrected here
	_ = writer.Close()

	req, err := http.NewRequest("POST", url, body)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer resp.Body.Close()

	// Read and print the response
	respBody, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("POST Response:", string(respBody))
}

type VCRequest struct {
	IMSI string `json:"IMSI"`
	DID  string `json:"DID"`
}

type P3Request struct {
	DID string               `json:"DID"`
	VC  VerifiableCredential `json:"VC"`
}

func main() {
	// ds := core.NewDIDService(KEY_STORE_PATH)
	// time.Sleep(10 * time.Second)

	UE_activate_baseline_time := time.Now()
	fmt.Println("UE activated time:", UE_activate_baseline_time)

	// print time to timelogs.txt
	file, err := os.OpenFile("timelogs.txt", os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	_, err = file.WriteString(UE_activate_baseline_time.Format("2006-01-02 15:04:05.000000000") + "\n")
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}

	IMSI := "208950000000031" //这个得修改

	fmt.Println("IMSI is :")
	fmt.Println(IMSI)

	//生成私钥
	privateKey, err := crypto.GenerateKey()
	//生成公钥
	publicKeyBytes := crypto.FromECDSAPub(&privateKey.PublicKey)

	// fmt.Printf("pk: %s\n", publicKeyBytes)
	// fmt.Println(publicKeyBytes)

	publicKey := hex.EncodeToString(publicKeyBytes[:])

	diddocument := document_generate(IMSI, privateKey, publicKey)

	byteDiddoc, err := json.Marshal(diddocument)
	if err != nil {
		fmt.Printf("fail in marshal didDocument.")
		panic(err)
	}
	fmt.Println("good diddoc is :", string(byteDiddoc))

	// =============== 与organization沟通 ================
	requestBody := VCRequest{
		IMSI: IMSI,
		DID:  diddocument.Id,
	}

	jsonBody, _ := json.Marshal(requestBody)

	req, err := http.NewRequest(
		"POST",
		"http://localhost:6080/get-vc",
		bytes.NewBuffer(jsonBody),
	)

	if err != nil {
		log.Fatal("创建请求失败:", err)
	}

	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}

	resp, err := client.Do(req)
	if err != nil {
		log.Fatal("请求发送失败：", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		log.Fatalf("请求失败 [%d]: %s", resp.StatusCode, body)
	}

	var vc VerifiableCredential
	if err := json.NewDecoder(resp.Body).Decode(&vc); err != nil {
		log.Fatal("响应解析失败：", err)
	}

	fmt.Println("=== 成功获取可验证凭证 ===")
	fmt.Printf("vc：%s\n", vc)
	fmt.Printf("颁发机构：%s\n", vc.Issuer)
	fmt.Printf("用户DID：%s\n", vc.CredentialSubject.ID)
	fmt.Printf("数字签名：%s\n", vc.Proof.SignatureValue)

	// =============== 与发送p3-chain ================

	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	_ = writer.WriteField("DID", diddocument.Id)

	vcJSON, _ := json.Marshal(vc)
	_ = writer.WriteField("VC", string(vcJSON))

	writer.Close()

	req, err = http.NewRequest(
		"POST",
		"http://127.0.0.1:8004/dper/setdid_baseline",
		body,
	)

	if err != nil {
		log.Fatal("创建请求失败:", err)
	}

	req.Header.Set("Content-Type", writer.FormDataContentType())

	client = &http.Client{}

	resp, err = client.Do(req)
	if err != nil {
		log.Fatal("请求发送失败：", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		log.Fatal("请求失败 [%d]: %s", resp.StatusCode, body)

	}

	fmt.Println(resp.Body)

	// time.Sleep(100 * time.Second)

}

package main

import (
	"bytes"
	"crypto/ecdsa"
	"crypto/sha256"
	"didserver_local/crypto"
	"didserver_local/httpclient"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

const KEY_STORE_PATH = "./keystore"

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

// 需要自己更改的http端口！！！！！！！！！！！！！
var pathHttp = "127.0.0.1:8004"
var listenpath = "127.0.0.1:8008"

// 发送message请求签名
func sig_request(message string) string {
	response, err := httpclient.SendPOST("http://"+pathHttp+"/dper/signaturereturn", "application/json", []byte(message))
	if err != nil {
		fmt.Println("Error:", err)

	}
	fmt.Println("POST Response:", response)

	var respSignData sigResponse
	err = json.Unmarshal([]byte(response), &respSignData)
	if err != nil {
		panic(err)
	}
	sign := respSignData.Signature
	return sign
}

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

func main() {
	// ds := core.NewDIDService(KEY_STORE_PATH)
	r := gin.Default()
	var totalDuration time.Duration

	r.POST("/hello", func(c *gin.Context) {
		//开始时间记录
		start := time.Now()
		elapsed := time.Since(start)
		totalDuration += elapsed
		fmt.Printf("收到imsi: %s\n", elapsed)

		byteArray, err := ioutil.ReadAll(c.Request.Body)
		if err != nil {
			c.String(http.StatusBadRequest, "Error reading request body")
			return
		}

		fmt.Printf("byteArray is %s\n", byteArray)

		err = json.Unmarshal(byteArray, &dq)
		if err != nil {
			c.String(http.StatusBadRequest, "Error parsing request body")
			return
		}
		elapsed = time.Since(start)
		totalDuration += elapsed
		fmt.Printf("解析得到imsi: %s\n", elapsed)

		// dq.DID = "208950000000031"

		fmt.Println("IMSI is :")
		fmt.Println(dq.DID)
		// newArgs := "did:" + dq.DID
		// // var args [][]byte

		// // for i := 0; i < len(dq.DID); i++ {
		// // 	b, _ := strconv.Atoi(string(dq.DID[i]))
		// // 	args = append(args, []byte{byte(b)})
		// // }
		// args := [][]byte{[]byte(newArgs)}

		// fmt.Println(args)

		// tempUser := ds.CreateLocalUser("")
		// tx := ds.BuildTransaction(tempUser, "SampleContract", "SampleFunction", args)

		// byteTx, err := json.Marshal(tx)
		// if err != nil {
		// 	fmt.Printf("fail in marshal tx.")
		// 	panic(err)
		// }
		// // fmt.Println(byteTx)

		// strTx := string(byteTx)

		// print(strTx)

		// // sendGet to get the address
		// fmt.Println("Going to get the address")
		// accountResponse, err := httpclient.SendGET("http://" + pathHttp + "/dper/accountsList")
		// if err != nil {
		// 	fmt.Println("Error:", err)
		// 	return
		// }
		// fmt.Println("GET Response:", accountResponse)

		// var respData AccountResponse
		// err = json.Unmarshal([]byte(accountResponse), &respData)
		// if err != nil {
		// 	panic(err)
		// }
		// var accountValue string
		// if len(respData.Data.Accounts) > 0 {
		// 	accountValue = respData.Data.Accounts[0]
		// 	accountValue = accountValue[1 : len(accountValue)-1]
		// 	fmt.Println("Account Value:", accountValue)
		// } else {
		// 	fmt.Println("No account value found")
		// }

		// fmt.Printf("IMSI is %s\n", dq.DID)

		// diddocument := document_generate(dq.DID, accountValue)
		// fmt.Println("diddocument is :", diddocument)

		// // Send the first request
		// sendFormDataRequest2("http://"+pathHttp+"/dper/useAccount", accountValue, " ")

		//生成私钥
		privateKey, err := crypto.GenerateKey()
		//生成公钥
		publicKeyBytes := crypto.FromECDSAPub(&privateKey.PublicKey)

		elapsed = time.Since(start)
		totalDuration += elapsed
		fmt.Printf("公私钥对生成时间: %s\n", elapsed)

		// fmt.Printf("pk: %s\n", publicKeyBytes)
		fmt.Println(publicKeyBytes)

		publicKey := hex.EncodeToString(publicKeyBytes[:])

		diddocument := document_generate(dq.DID, privateKey, publicKey)

		elapsed = time.Since(start)
		totalDuration += elapsed
		fmt.Printf("did、document生成时间: %s\n", elapsed)

		// url := "http://" + listenpath + "/dper/getimsi"
		// method := "POST"

		// // fmt.Printf("IMSI is %s\n", dq.DID)
		// fmt.Printf("DID is %s\n", diddocument.Id)

		// payload := &bytes.Buffer{}
		// writer := multipart.NewWriter(payload)
		// _ = writer.WriteField("DID", diddocument.Id)
		// _ = writer.WriteField("IMSI", dq.DID)
		// err = writer.Close()
		// if err != nil {
		// 	fmt.Println(err)
		// 	return
		// }

		// client := &http.Client{}
		// req, err := http.NewRequest(method, url, payload)

		// if err != nil {
		// 	fmt.Println(err)
		// 	return0x44
		// if err != nil {
		// 	fmt.Println(err)
		// 	return
		// }
		// defer res.Body.Close()

		// body, err := ioutil.ReadAll(res.Body)
		// if err != nil {
		// 	fmt.Println(err)
		// 	return
		// }
		// fmt.Println(body)

		// sendFormDataRequest4("http://"+listenpath+"/dper/getimsi", "IMSI", dq.DID, "DID", diddocument.Id)

		byteDiddoc, err := json.Marshal(diddocument)
		if err != nil {
			fmt.Printf("fail in marshal didDocument.")
			panic(err)
		}
		fmt.Println("good diddoc is :", byteDiddoc)

		// c.String(http.StatusOK, string(byteDiddoc))
		// var lessDid didDocument
		// lessDid.Id = "DID:123456789"
		// lessDid.Pk = "9f002199d3887fbc46574d0400148bb631010c17"
		// byteDiddoc2, err := json.Marshal(lessDid)
		fmt.Printf(" less diddoc is :\n", string(byteDiddoc))
		if err != nil {
			fmt.Printf("fail in marshal didDocument.")
			panic(err)
		}
		c.String(http.StatusOK, string(byteDiddoc))
		elapsed = time.Since(start)
		totalDuration += elapsed
		fmt.Printf("返回diddocument时间: %s\n", elapsed)

	})
	// 最早这里是8080
	if err := r.Run(":8080"); err != nil {
		panic(err)
	}
}

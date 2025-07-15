// 25-04-07 现在要解决的是，如何将合法的organization publickey提前定义存储并使用

package main

import (
	"Organization/crypto"
	"crypto/ecdsa"
	"crypto/sha256"

	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"
	"time"
)

var (
	privateKeyHex = "0AA0C9B06BB042357D8DA5310D87348FB2EF245BF118E78DF6B95F9D02356755"
	publicKeyHex  = "04BE4F1BA1BD5C59E85C2BB6B3FAF99FD161DF9845B0C4E6363F110FB27DB65A76CBF5759CCC447327702FB9D32E827ED01DF7B9D7F6583C8F52BE2421E9A40F2B"
)

// 可验证声明(VC)数据结构
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

// 内存中存储的合法IMSI列表（实际应存储在数据库）
var validIMSIs = map[string]bool{
	"460001234567890": true, // 示例IMSI
}

// 机构私钥（生产环境应使用安全存储方案）
// var issuerPrivateKey *rsa.PrivateKey
var privateKey *ecdsa.PrivateKey

func main() {

	privateKeyBytes, err := hex.DecodeString(privateKeyHex)
	if err != nil {
		log.Fatal("私钥加载失败：", err)
	}

	privateKey = crypto.ToECDSA(privateKeyBytes)
	if err != nil {
		log.Fatal("私钥加载失败", err)
	}

	publicKeyBytes := crypto.FromECDSAPub(&privateKey.PublicKey)
	if strings.ToUpper(hex.EncodeToString(publicKeyBytes)) != publicKeyHex {
		log.Fatal("公钥与私钥不匹配")
	}
	fmt.Println("已加载预生成密钥对")

	// 2. 启动HTTP服务
	http.HandleFunc("/get-vc", handleVCRequest)
	fmt.Println("机构服务器启动，监听 :6080...")
	log.Fatal(http.ListenAndServe(":6080", nil))
}

// 处理VC请求
func handleVCRequest(w http.ResponseWriter, r *http.Request) {
	// 解析IMSI参数
	// IMSI := r.URL.Query().Get("IMSI")
	// DID := r.URL.Query().Get("DID")
	

	startTime := time.Now()
	genKeyPair()

	// 打印请求基本信息
	log.Printf("👉 收到请求: %s %s", r.Method, r.URL.Path)

	// ...原有处理逻辑...

	var request struct {
		IMSI string `json:"IMSI"`
		DID  string `json:"DID"`
	}

	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		http.Error(w, "无效请求体", http.StatusBadRequest)
		return
	}

	IMSI := request.IMSI
	DID := request.DID

	if IMSI == "" {
		http.Error(w, "缺少IMSI参数", http.StatusBadRequest)
		return
	}

	if DID == "" {
		http.Error(w, "缺少DID参数", http.StatusBadRequest)
		return
	}

	// 验证IMSI合法性
	// if !isValidIMSI(IMSI) {
	// 	http.Error(w, "无效的IMSI", http.StatusNotFound)
	// 	return
	// }

	// 生成VC并签名
	vc, err := generateVC(IMSI, DID, privateKey)
	if err != nil {
		http.Error(w, "VC生成失败", http.StatusInternalServerError)
		return
	}

	// 返回JSON响应
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(vc)

	// 记录处理完成信息
	log.Printf("✅ 请求处理完成 [%s] | 耗时: %v", r.URL.Path, time.Since(startTime))

}

// 验证IMSI有效性
func isValidIMSI(IMSI string) bool {
	// 1. 检查长度是否符合规范（15位）
	if len(IMSI) != 15 {
		return false
	}

	// 2. 检查是否在授权列表中
	return validIMSIs[IMSI]
}

// // 生成密钥对
func genKeyPair() {
	var err error
	// issuerPrivateKey, err = rsa.GenerateKey(rand.Reader, 2048)
	privateKey, err = crypto.GenerateKey()
	privateBytes := crypto.FromECDSA(privateKey)
	fmt.Printf("// 私钥（Hex）\nvar privateKeyHex = \"%X\" \n\n", privateBytes)

	publicKeyBytes := crypto.FromECDSAPub(&privateKey.PublicKey)
	fmt.Printf("// 公钥（Hex）\nvar publicKeyHex = \"%X\" \n\n", publicKeyBytes)

	// fmt.Printf("pk: %s\n", publicKeyBytes)
	// fmt.Println(publicKeyBytes)

	// publicKey := hex.EncodeToString(publicKeyBytes[:])
	if err != nil {
		log.Fatal("密钥生成失败:", err)
	}
}

// 生成并签名VC
func generateVC(IMSI string, DID string, privateKey *ecdsa.PrivateKey) (*VerifiableCredential, error) {
	// 1. 构造VC基础数据
	vc := VerifiableCredential{
		Context:      []string{"https://www.w3.org/2018/credentials/v1"},
		Type:         []string{"VerifiableCredential", "IMSIIdentityCredential"},
		Issuer:       "did:telecom:china-mobile", // 机构DID
		IssuanceDate: time.Now().Format(time.RFC3339),
	}
	vc.CredentialSubject.ID = DID // 用户DID
	vc.CredentialSubject.IMSI = IMSI
	vc.CredentialSubject.Carrier = "中国移动"

	// 2. 准备签名数据
	signData, _ := json.Marshal(vc.CredentialSubject)
	hashed := sha256.Sum256(signData)

	// 3. 使用私钥签名
	// signature, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, hashed[:])
	signature, err := crypto.Sign(hashed[:], privateKey)
	if err != nil {
		return nil, err
	}

	// 4. 填充签名信息
	vc.Proof.Type = "RsaSignature2024"
	vc.Proof.Created = time.Now().Format(time.RFC3339)
	vc.Proof.ProofPurpose = "assertionMethod"
	vc.Proof.VerificationMethod = "did:telecom:china-mobile#keys-1" // 公钥地址
	vc.Proof.SignatureValue = hex.EncodeToString(signature)

	return &vc, nil
}

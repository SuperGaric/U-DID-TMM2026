package client

import (
	"bytes"
	"dper/common"
	"dper/eles"
	"fmt"
	"mime/multipart"

	"github.com/ethereum/go-ethereum/rlp"
)

// 在目标dper上创建新账户，返回值是账户地址
func NewAccount(dperurl, password string) common.Address {
	// 创建一个缓冲区，用于存储multipart/form-data请求的内容
	var buf bytes.Buffer
	// 创建一个multipart.Writer实例，用于构建multipart/form-data请求的body
	writer := multipart.NewWriter(&buf)
	// 添加form-data参数
	writer.WriteField("password", password)

	writer.Close()

	addrStr := sendHttpPost(dperurl, buf, writer)
	addr := common.HexToAddress(addrStr)

	return addr
}

// 请求dper节点自生成一条交易并完成共识上链
func SoftInvokeAndCall(dperurl, contractName, functionName, args string) string {

	// 创建一个缓冲区，用于存储multipart/form-data请求的内容
	var buf bytes.Buffer
	// 创建一个multipart.Writer实例，用于构建multipart/form-data请求的body
	writer := multipart.NewWriter(&buf)
	// 添加form-data参数
	writer.WriteField("contractName", contractName)
	writer.WriteField("functionName", functionName)
	writer.WriteField("args", args)

	writer.Close()

	return sendHttpPost(dperurl, buf, writer)
}

// 请求dper节点自生成一条交易并完成共识上链
func SolidInvokeAndCall(dperurl, contractAddr, functionAddr, args string) string {

	// 创建一个缓冲区，用于存储multipart/form-data请求的内容
	var buf bytes.Buffer
	// 创建一个multipart.Writer实例，用于构建multipart/form-data请求的body
	writer := multipart.NewWriter(&buf)
	// 添加form-data参数
	writer.WriteField("contractName", contractAddr)
	writer.WriteField("functionName", functionAddr)
	writer.WriteField("args", args)

	writer.Close()

	return sendHttpPost(dperurl, buf, writer)
}

// 查询某交易的回执(验证是否上链)
func BackTransactionReceipt(dperUrl string, txID string) string {
	// 创建一个缓冲区，用于存储multipart/form-data请求的内容
	var buf bytes.Buffer
	// 创建一个multipart.Writer实例，用于构建multipart/form-data请求的body
	writer := multipart.NewWriter(&buf)
	// 添加form-data参数
	writer.WriteField("txID", txID)

	writer.Close()

	return sendHttpPost(dperUrl, buf, writer)
}

// 在客户端本地生成若干条交易，rlp编码后发送到dper进行共识上链
func PublishTx(url string, txList []*eles.Transaction) (error, string) {

	txGroup := eles.NewTransactionGroup(txList)
	payload, err := rlp.EncodeToBytes(txGroup)
	if err != nil {
		fmt.Printf("交易集合rlp编码失败,err:%v\n", err)
		return err, ""
	}
	var buf bytes.Buffer
	buf.Write(payload)

	resp := sendHttpPost(url, buf, nil)

	return nil, resp
}

// 请求目标dper返回当前已上链的交易总数
func GetTransactionNumber(dperurl string) string {
	return sendHttpGet(dperurl)
}

// 请求目标dper返回当前头区块的hash值
func GetCurrentBlockHash(dperurl string) string {
	return sendHttpGet(dperurl)
}

func OpenTxCheckMode(dperUrl string, mode string) string {
	// 创建一个缓冲区，用于存储multipart/form-data请求的内容
	var buf bytes.Buffer
	// 创建一个multipart.Writer实例，用于构建multipart/form-data请求的body
	writer := multipart.NewWriter(&buf)
	// 添加form-data参数
	writer.WriteField("mode", mode)

	writer.Close()

	return sendHttpPost(dperUrl, buf, writer)
}

func CloseTxCheckMode(dperUrl string, mode string) string {
	// 创建一个缓冲区，用于存储multipart/form-data请求的内容
	var buf bytes.Buffer
	// 创建一个multipart.Writer实例，用于构建multipart/form-data请求的body
	writer := multipart.NewWriter(&buf)
	// 添加form-data参数
	writer.WriteField("mode", mode)

	writer.Close()

	return sendHttpPost(dperUrl, buf, writer)
}

func BackViewNetInfo(dperUrl string) string {
	return sendHttpGet(dperUrl)
}

func BackTPBFT(dperUrl string) string {
	return sendHttpGet(dperUrl)
}

func BackContract(dperUrl string) string {
	return sendHttpGet(dperUrl)
}

func BackBlockNum(dperUrl string) string {
	return sendHttpGet(dperUrl)
}

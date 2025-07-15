package client

import (
	"dper/accounts"
	"dper/common"
	"dper/contract"
	"dper/crypto/keys"
	"dper/eles"
	"encoding/json"
	"fmt"
	"math/rand"
	"reflect"
	"strconv"
	"time"
)

type Client struct {
	Url      string
	Port     int
	KeyStore keys.KeyStore

	PassWord       string
	CurAccount     *accounts.Account
	AccountManager *accounts.Manager

	RemoteAccount *accounts.Account

	// TxCheckMode bool
}

func NewClient(url string, port int, keyStoreDir string, pwd string) *Client {
	client := &Client{
		Url:      url,
		Port:     port,
		KeyStore: keys.NewKeyStorePassphrase(keyStoreDir),
		PassWord: pwd,
		//TxCheckMode: false,
	}
	client.AccountManager = accounts.NewManager(client.KeyStore)
	client.CurAccount, _ = client.AccountManager.NewAccount(pwd)

	return client
}

// 切换当前CurAccount
func (user *Client) ChangeAccount(addr common.Address) bool {
	if account, err := user.AccountManager.GetAccount(addr); err != nil {
		return false
	} else {
		user.CurAccount = account
		return true
	}
}

// 在本地产生指定数量的不重复交易，发送给目标client
func (user *Client) PublishTransactionSolid(contractAddr common.Address, functionAddr common.Address, argStr []string, txCount int) (string, []string) {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/publishTx"

	if reflect.DeepEqual(contractAddr, common.Address{}) {
		contractAddr = contract.StringToContractAddress("DEMO1")
	}
	if reflect.DeepEqual(functionAddr, common.Address{}) {
		functionAddr = contract.StringToFunctionAddress("set")
	}
	if len(argStr) == 0 {
		argStr = []string{"test_arg", "xxxx"}
	}

	version := user.QueryCurrentBlockHash() // 最新的头区块哈希

	args := make([][]byte, 0) // 交易内包含的内容
	for _, str := range argStr {
		args = append(args, []byte(str))
	}

	// 使用注册的account进行签名
	txID := make([]string, 0)

	txs := make([]*eles.Transaction, 0)
	for i := 0; i < txCount; i++ {
		tx := eles.Transaction{
			Sender:    user.CurAccount.Address,
			Nonce:     uint64(i),
			Version:   version,
			LifeTime:  0,
			Contract:  contractAddr,
			Function:  functionAddr,
			Args:      args,
			CheckList: make([]eles.CheckElement, 0),
		}
		tx.SetTxID()

		signature, err := user.AccountManager.SignHash(*user.CurAccount, tx.TxID) // 账户私钥进行签名
		if err != nil {
			fmt.Printf("Transaction generation failed, signature failed, err:%v\n", err)
			continue
		}
		tx.Signature = signature

		txs = append(txs, &tx)

		txID = append(txID, fmt.Sprintf("%x", tx.TxID))
	}

	_, resp := PublishTx(dperUrl, txs)

	return resp, txID
}

func (user *Client) PublishTransactionSoft(contractName string, functionName string, argStr []string, txCount int) (string, []string) {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/publishTx"

	if contractName == "" {
		contractName = "DEMO1"
	}
	if functionName == "" {
		functionName = "set"
	}
	if len(argStr) == 0 {
		argStr = []string{"test_arg", "xxxx"}
	}

	contractAddr := contract.StringToContractAddress(contractName) // 合约地址
	functionAddr := contract.StringToFunctionAddress(functionName) // 函数地址

	version := user.QueryCurrentBlockHash() // 最新的头区块哈希

	args := make([][]byte, 0) // 交易内包含的内容
	for _, str := range argStr {
		args = append(args, []byte(str))
	}

	// 使用注册的account进行签名
	txID := make([]string, 0)

	txs := make([]*eles.Transaction, 0)
	for i := 0; i < txCount; i++ {
		tx := eles.Transaction{
			Sender:    user.CurAccount.Address,
			Nonce:     uint64(i),
			Version:   version,
			LifeTime:  0,
			Contract:  contractAddr,
			Function:  functionAddr,
			Args:      args,
			CheckList: make([]eles.CheckElement, 0),
		}
		tx.SetTxID()

		signature, err := user.AccountManager.SignHash(*user.CurAccount, tx.TxID) // 账户私钥进行签名
		if err != nil {
			fmt.Printf("Transaction generation failed, signature failed, err:%v\n", err)
			continue
		}
		tx.Signature = signature

		txs = append(txs, &tx)

		txID = append(txID, fmt.Sprintf("%x", tx.TxID))
	}

	_, resp := PublishTx(dperUrl, txs)

	return resp, txID
}

// 查询最新的头区块hash
func (user *Client) QueryCurrentBlockHash() common.Hash {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/block/blockHash"
	curVersionStr := GetCurrentBlockHash(dperUrl)
	//fmt.Printf("[%s]上一区块hash:%s\n", time.Now().Format("2006-01-02 15:04:05"), curVersionStr)
	return common.HexToHash(curVersionStr)
}

func randomKey() int {
	rand.Seed(time.Now().UnixNano())
	randomkey := rand.Intn(1000000)
	return randomkey
}

type TransactionReceipt struct {
	Code int     `json:"code"`
	Data Receipt `json:"data"`
	Msg  string  `json:"msg"`
}

type Receipt struct {
	TXID   string `json:"Transaction ID"`
	Valid  bool   `json:"Valid"`
	Result string `json:"Transaction Results"`
	Delay  string `json:"Consensus Delay"`
}

func (user *Client) InvokeTransactionSoft(contractName string, functionName string, argStr []string, txCheckMode bool) {
	dperPort := strconv.Itoa(user.Port)

	sendTime := time.Now()
	receiveTime := sendTime

	resp, txID := user.PublishTransactionSoft(contractName, functionName, argStr, 1)
	if resp == "" { // 属于是上链失败
		fmt.Printf("Transaction upload failed\n")
		return
	}

	if txCheckMode {
		for i := 0; i < 4; i++ {
			dperUrl := user.Url + dperPort + "/dper/queryTx"
			receipt := BackTransactionReceipt(dperUrl, txID[0])

			txReceipt := TransactionReceipt{}
			json.Unmarshal([]byte(receipt), &txReceipt)

			if !txReceipt.Data.Valid {
				time.Sleep(500 * time.Millisecond)
				continue
			} else {
				receiveTime = time.Now()
				interval := receiveTime.Sub(sendTime)
				txReceipt.Data.Delay = fmt.Sprintf("%d ms", interval.Milliseconds())

				fmt.Printf("Transaction ID: %s\n", txReceipt.Data.TXID)
				fmt.Printf("valid: %v\n", txReceipt.Data.Valid)
				fmt.Printf("Transaction Results: %s\n", txReceipt.Data.Result)
				fmt.Printf("Consensus Delay: %s\n", txReceipt.Data.Delay)
				return
			}
		}
	} else {
		return
	}

}

func (user *Client) InvokeTransactionSolid(contractAddr string, functionAddr string, argStr []string, txCheckMode bool) {
	dperPort := strconv.Itoa(user.Port)

	sendTime := time.Now()
	receiveTime := sendTime

	resp, txID := user.PublishTransactionSolid(contract.StringToContractAddress(contractAddr), contract.StringToContractAddress(functionAddr), argStr, 1)
	if resp == "" { // 属于是上链失败
		fmt.Printf("Transaction upload failed\n")
		return
	}

	if txCheckMode {
		for i := 0; i < 4; i++ {
			dperUrl := user.Url + dperPort + "/dper/queryTx"
			receipt := BackTransactionReceipt(dperUrl, txID[0])

			txReceipt := TransactionReceipt{}
			json.Unmarshal([]byte(receipt), &txReceipt)

			if !txReceipt.Data.Valid {
				time.Sleep(500 * time.Millisecond)
				continue
			} else {
				receiveTime = time.Now()
				interval := receiveTime.Sub(sendTime)
				txReceipt.Data.Delay = fmt.Sprintf("%d ms", interval.Milliseconds())

				fmt.Printf("Transaction ID: %s\n", txReceipt.Data.TXID)
				fmt.Printf("valid: %v\n", txReceipt.Data.Valid)
				fmt.Printf("Transaction Results: %s\n", txReceipt.Data.Result)
				fmt.Printf("Consensus Delay: %s\n", txReceipt.Data.Delay)
				return
			}
		}
	} else {
		return
	}
}

type CallResult struct {
	Code int      `json:"code"`
	Data []string `json:"data"`
	Msg  string   `json:"msg"`
}

func (user *Client) CallTransactionSoft(contractName string, functionName string, argStr []string) {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/softCall"
	args := ""
	for _, arg := range argStr {
		args += arg + " "
	}

	resp := SoftInvokeAndCall(dperUrl, contractName, functionName, args)

	callRes := CallResult{}
	json.Unmarshal([]byte(resp), &callRes)

	if !reflect.DeepEqual(callRes, CallResult{}) {
		fmt.Printf("Call Result: %v\n", callRes.Data)
	}
}

func (user *Client) CallTransactionSolid(contractAddr string, functionAddr string, argStr []string) {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/solidCall"
	args := ""
	for _, arg := range argStr {
		args += arg + " "
	}

	resp := SoftInvokeAndCall(dperUrl, contractAddr, functionAddr, args)

	callRes := CallResult{}
	json.Unmarshal([]byte(resp), &callRes)

	if !reflect.DeepEqual(callRes, CallResult{}) {
		fmt.Printf("Call Result: %v\n", callRes.Data)
	}
}

type TransactionCount struct {
	Code int    `json:"code"`
	Data int    `json:"data"`
	Msg  string `json:"msg"`
}

// 查询已上链的交易数量
func (user *Client) QueryTransactionCount() int {

	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/block/getTransactionNumber"

	infoStr := GetTransactionNumber(dperUrl)
	txCount := TransactionCount{}

	json.Unmarshal([]byte(infoStr), &txCount)

	return txCount.Data

	//fmt.Printf("[%s]链上交易数目:%s\n", time.Now().Format("2006-01-02 15:04:05"), GetTransactionNumber(dperUrl))
	//return nil
}

// 请求dper节点开通一个新账户，返回值为新创建的账户
func (user *Client) CreateNewAccount(password string) *accounts.Account {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/newAccount"
	accountHash := NewAccount(dperUrl, password)

	return &accounts.Account{Address: accountHash}
}

func (user *Client) OpenTxCheckMode() {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/txCheck"

	res := OpenTxCheckMode(dperUrl, "on")

	fmt.Println(res)

}

func (user *Client) CloseTxCheckMode() {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/txCheck"

	res := OpenTxCheckMode(dperUrl, "close")

	fmt.Println(res)
}

type DPNetWork struct {
	Booters []string       `json:"booters"`
	Leaders []string       `json:"leaders"`
	SubNets []DPSubNetwork `json:"subnets"`
}

type DPSubNetwork struct {
	Leader    string   `json:"leader"`
	NetID     string   `json:"netID"`
	Followers []string `json:"followers"`
}

type ViewNetInfo struct {
	Code int       `json:"code"`
	Data DPNetWork `json:"data"`
	Msg  string    `json:"msg"`
}

func (user *Client) BackViewNetInfo() {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/network/networkInfo"

	viewNetStr := BackViewNetInfo(dperUrl)

	viewNet := ViewNetInfo{}

	json.Unmarshal([]byte(viewNetStr), &viewNet)

	fmt.Println("Upper Channel: ")
	fmt.Println("node Count: ", len(viewNet.Data.Booters)+len(viewNet.Data.Leaders))
	for i := 0; i < len(viewNet.Data.Booters); i++ {
		fmt.Printf("Booter%d: %s\n", i, viewNet.Data.Booters[i])
	}
	for i := 0; i < len(viewNet.Data.Leaders); i++ {
		fmt.Printf("Leader%d: %s\n", i, viewNet.Data.Leaders[i])
	}

	fmt.Println()
	fmt.Println("Lower Channel: ")
	for i := 0; i < len(viewNet.Data.SubNets); i++ {
		fmt.Println("netID: ", viewNet.Data.SubNets[i].NetID)
		fmt.Println("node Count: ", len(viewNet.Data.SubNets[i].Followers)+1)
		fmt.Printf("Leader: %s\n", viewNet.Data.SubNets[i].Leader)

		for j := 0; j < len(viewNet.Data.SubNets[i].Followers); j++ {
			fmt.Printf("Follower%d: %s\n", j, viewNet.Data.SubNets[i].Followers[j])
		}
		fmt.Println()
	}
}

type TPBFTInfo struct {
	Code int      `json:"code"`
	Data []string `json:"data"`
	Msg  string   `json:"msg"`
}

func (user *Client) BackTPBFT() {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/TPBFT"

	tpbftStr := BackTPBFT(dperUrl)
	tpbft := TPBFTInfo{}
	json.Unmarshal([]byte(tpbftStr), &tpbft)

	fmt.Println("Currently used lower consensus protocols:", tpbft.Data)
}

type ContractInfo struct {
	Code int    `json:"code"`
	Data string `json:"data"`
	Msg  string `json:"msg"`
}

func (user *Client) BackContract() {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/dper/contract"

	contractStr := BackContract(dperUrl)
	contract := ContractInfo{}
	json.Unmarshal([]byte(contractStr), &contract)

	contracts := make([]string, 0)
	if contract.Data == "DEMO_CONTRACT_MIX123" {
		contracts = append(contracts, "DEMO1")
		contracts = append(contracts, "DEMO2")
	} else {
		contracts = append(contracts, contract.Data)
	}

	fmt.Println("Currently used consensus contracts:", contracts)
}

type BlockNumInfo struct {
	Code int    `json:"code"`
	Data int    `json:"data"`
	Msg  string `json:"msg"`
}

func (user *Client) GetBlockNum() {
	dperPort := strconv.Itoa(user.Port)
	dperUrl := user.Url + dperPort + "/block/blockNumber"

	blockNumStr := BackBlockNum(dperUrl)
	bn := new(BlockNumInfo)
	json.Unmarshal([]byte(blockNumStr), &bn)

	count := bn.Data

	fmt.Println("Current total number of blocks:", count)
}

package core

import (
	"UE/accounts"
	"UE/common"
	"UE/contract"
	"UE/crypto/keys"
	"UE/eles"

	"github.com/ethereum/go-ethereum/rlp"
)

type DIDService struct {
	accountManager *accounts.Manager
}

func NewDIDService(keyStorePath string) *DIDService {
	keyStore := keys.NewKeyStorePassphrase(keyStorePath)
	accountMangager := accounts.NewManager(keyStore)
	return &DIDService{accountManager: accountMangager}
}

func (ds *DIDService) CreateLocalUser(password string) *accounts.Account {
	account, err := ds.accountManager.NewAccount(password)
	if err != nil {
		panic(err)
	}

	ds.accountManager.Unlock(account.Address, password)
	return account
}

func (ds *DIDService) BuildTransaction(user *accounts.Account, contractName string, functionName string, args [][]byte) *eles.Transaction {

	tx := eles.Transaction{
		Sender:    user.Address,
		Nonce:     0,
		Version:   common.Hash{},
		LifeTime:  0,
		Contract:  contract.StringToContractAddress(contractName),
		Function:  contract.StringToFunctionAddress(functionName),
		Args:      args,
		CheckList: make([]eles.CheckElement, 0),
	}

	tx.SetTxID()
	signature, err := ds.accountManager.SignHash(*user, tx.TxID)
	if err != nil {
		panic(err)
	}
	tx.Signature = signature
	return &tx
}

func (ds *DIDService) CompressTransaction(tx *eles.Transaction) []byte {
	res, err := rlp.EncodeToBytes(tx)
	if err != nil {
		panic(err)
	}
	return res
}

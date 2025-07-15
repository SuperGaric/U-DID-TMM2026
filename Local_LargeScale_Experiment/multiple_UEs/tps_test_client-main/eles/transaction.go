package eles

import (
	"dper/common"
	"dper/crypto"
	"fmt"

	"github.com/ethereum/go-ethereum/rlp"
)

type Transaction struct {
	// head
	TxID      common.Hash
	Sender    common.Address
	Nonce     uint64
	Version   common.Hash
	LifeTime  uint8 // the max lagging versions after the current one
	Signature []byte

	//body
	Contract common.Address
	Function common.Address
	Args     [][]byte // function argument

	//tail
	CheckList []CheckElement //
}

type CheckElement struct {
	CheckType    uint8
	ValueAddress common.WsKey
	Value        []byte
}

func (tx *Transaction) Hash() common.Hash {
	plainTx := *tx
	plainTx.TxID = common.Hash{}
	plainTx.Signature = []byte{}
	summary, err := rlp.EncodeToBytes(&plainTx)
	if err != nil {
		fmt.Println("fail in transaction hash!")
	}
	return crypto.Sha3Hash(summary)
}

func (tx *Transaction) SetTxID() {
	tx.TxID = tx.Hash()
}

func GenerateCheckElement(valueAddr common.WsKey, value []byte, checkType uint8) CheckElement {
	checkEle := CheckElement{
		CheckType:    checkType,
		ValueAddress: valueAddr,
		Value:        value,
	}
	return checkEle
}

type TransactionGroup struct {
	Txs []Transaction
}

func (tg *TransactionGroup) BackGroup() []Transaction {
	return tg.Txs
}

func NewTransactionGroup(txs []*Transaction) *TransactionGroup {
	plainTxs := make([]Transaction, len(txs))
	for i := 0; i < len(txs); i++ {
		plainTxs[i] = *txs[i]
	}
	return &TransactionGroup{Txs: plainTxs}

}

package commandline

import (
	"dper/accounts"
	"dper/common"
	loglogrus "dper/loglogrus"
	"fmt"
)

func (c *CommandLine) printAccounts(accounts []accounts.Account) string {
	info := fmt.Sprintf("Got %d accounts:\n", len(accounts))
	for i := 0; i < len(accounts); i++ {
		info += fmt.Sprintf("No.%d, Address: %x\n", i, accounts[i].Address)
	}
	fmt.Print(info)
	return info
}

func (c *CommandLine) handleCreateLocalNewAccounts(arrs []string) (common.Address, error) {
	if len(arrs) == 1 {
		account, err := c.User.AccountManager.NewAccount("")
		if err != nil {
			return common.Address{}, err
		}
		c.User.CurAccount = account
		c.User.AccountManager.Unlock(account.Address, "")
		return account.Address, nil
	}
	if len(arrs) >= 2 {
		switch arrs[1] {
		case "-p", "-password":
		default:
			loglogrus.Log.Info("Dper: Please note -- You have not set a password for your account!\n")
			return common.Address{}, fmt.Errorf("should input password")
		}
		if len(arrs) == 2 {
			account, err := c.User.AccountManager.NewAccount("")
			if err != nil {
				return common.Address{}, err
			}
			c.User.CurAccount = account
			c.User.AccountManager.Unlock(account.Address, "")
			loglogrus.Log.Info("Dper: Please note -- The password you set for the account (%x) is an empty string!\n", account.Address)
			return account.Address, nil
		}
		if len(arrs) == 3 {
			account, err := c.User.AccountManager.NewAccount(arrs[2])
			if err != nil {
				return common.Address{}, err
			}
			c.User.CurAccount = account
			err = c.User.AccountManager.Unlock(account.Address, arrs[2])
			if err != nil {
				loglogrus.Log.Warnf("Dper failed: handleCreateNewAccounts can't Unlock specify account (%x)\n", account.Address)
				return common.Address{}, err
			}
			loglogrus.Log.Infof("Dper: New account (%x) created successfully!", account.Address)
			return account.Address, nil
		}
	}
	loglogrus.Log.Warnf("Dper: Create New Account is failed, because can't resolve the arguments!\n")
	return common.Address{}, fmt.Errorf("cannot resolve the arguments")
}

func (c *CommandLine) handleCreateRemoteNewAccounts(arrs []string) (common.Address, error) {
	if len(arrs) == 1 {
		account := c.User.CreateNewAccount("")
		c.User.RemoteAccount = account
		return account.Address, nil
	}
	if len(arrs) >= 2 {
		switch arrs[1] {
		case "-p", "-password":
		default:
			loglogrus.Log.Info("Dper: Please note -- You have not set a password for your account!\n")
			return common.Address{}, fmt.Errorf("should input password")
		}
		if len(arrs) == 2 {
			account := c.User.CreateNewAccount("")
			c.User.RemoteAccount = account
			loglogrus.Log.Info("Dper: Please note -- The password you set for the account (%x) is an empty string!\n", account.Address)
			return account.Address, nil
		}
		if len(arrs) == 3 {
			account := c.User.CreateNewAccount(arrs[2])
			c.User.RemoteAccount = account
			loglogrus.Log.Infof("Dper: New account (%x) created successfully!", account.Address)
			return account.Address, nil
		}
	}

	loglogrus.Log.Warnf("Dper: Create New Account is failed, because can't resolve the arguments!\n")
	return common.Address{}, fmt.Errorf("cannot resolve the arguments")
}

func (c *CommandLine) handleUseAccount(arrs []string) (common.Address, error) {
	if len(arrs) < 2 {
		loglogrus.Log.Warnf("Dper failed: handleUseAccount unmatched arguments, You should specify the address of the account!\n")
		return common.Address{}, fmt.Errorf("unmatched arguments")
	}
	accountAddr := common.HexToAddress(arrs[1])
	account, err := c.User.AccountManager.GetAccount(accountAddr)
	if err != nil {
		return common.Address{}, fmt.Errorf("account with address: %s cannot load, %v", arrs[1], err)
	}
	if len(arrs) == 2 {
		errr := c.User.AccountManager.Unlock(account.Address, "")
		if errr != nil {
			loglogrus.Log.Warnf("Dper failed: handleUseAccount can't Unlock specify account (%x)\n", account.Address)
			return common.Address{}, errr
		}
		c.User.CurAccount = account
		return c.User.CurAccount.Address, nil
	}
	if len(arrs) >= 3 {
		switch arrs[2] {
		case "-p", "-password":
		default:
			loglogrus.Log.Warnf("Dper failed: Please note -- You should input password to Login account(%x)!\n", accountAddr)
			return common.Address{}, fmt.Errorf("unmatched arguments")
		}
		if len(arrs) == 3 {
			errr := c.User.AccountManager.Unlock(account.Address, "")
			if errr != nil {
				loglogrus.Log.Warnf("Dper failed: handleUseAccount can't Unlock specify account (%x)\n", account.Address)
				return common.Address{}, errr
			}
			c.User.CurAccount = account
			loglogrus.Log.Infof("Dper: Successfully switched users. The current user is (%x)\n", c.User.CurAccount.Address)
			return c.User.CurAccount.Address, nil
		}
		if len(arrs) == 4 {
			errr := c.User.AccountManager.Unlock(account.Address, arrs[3])
			if errr != nil {
				loglogrus.Log.Warnf("Dper failed: handleUseAccount can't Unlock specify account (%x)\n", account.Address)
				return common.Address{}, errr
			}
			c.User.CurAccount = account
			loglogrus.Log.Infof("Dper: Successfully switched users. The current user is (%x)\n", c.User.CurAccount.Address)
			return c.User.CurAccount.Address, nil
		}
	}
	loglogrus.Log.Warnf("Dper: Switch current user account is failed, because can't resolve the arguments!\n")
	return common.Address{}, fmt.Errorf("cannot resolve the arguments")
}

func (c *CommandLine) printSelfInfo() string {
	info := ""
	info += fmt.Sprintf("Now used account address: %x\n", c.User.CurAccount.Address)
	fmt.Print(info)

	return info
}

func (c *CommandLine) handleTxCheckMode(arrs []string) error {
	if len(arrs) != 2 {
		loglogrus.Log.Warnf("Dper failed: handleTxCheckMode unmatched arguments!\n")
		return fmt.Errorf("unmatched arrguments is input")
	}
	switch arrs[1] {
	case "on", "start":
		c.txCheckMode = true
	case "off", "close", "stop":
		c.txCheckMode = false
	default:
		loglogrus.Log.Warnf("Dper failed: handleTxCheckMode unkown argument %s is input\n", arrs[1])
		return fmt.Errorf("unkown argument %s is input", arrs[1])
	}
	loglogrus.Log.Infof("Dper: handleTxCheckMode runs successfully, The current Tx check mode is %s\n", arrs[1])
	return nil
}

func (c *CommandLine) solidInvokeTransaction(arrs []string) error {
	if len(arrs) < 4 {
		loglogrus.Log.Warnf("Dper failed: solidInvokeTransaction unmatched arguments, Correct input format: invoke contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}
	if arrs[3] != "-args" {
		loglogrus.Log.Warnf("Dper failed: solidInvokeTransaction unmatched arguments, Correct input format: invoke contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}
	args := make([]string, 0)
	for i := 4; i < len(arrs); i++ {
		args = append(args, arrs[i])
	}

	c.User.InvokeTransactionSolid(arrs[1], arrs[2], args, c.txCheckMode)

	loglogrus.Log.Infof("Dper: solidInvokeTransaction runs successfully, transaction has been upload blockChain!\n")
	return nil
}

func (c *CommandLine) solidCallTransaction(arrs []string) error {

	if len(arrs) < 4 {
		loglogrus.Log.Warnf("Dper failed: solidCallTransaction unmatched arguments, Correct input format: call contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}
	if arrs[3] != "-args" {
		loglogrus.Log.Warnf("Dper failed: solidCallTransaction unmatched arguments, Correct input format: call contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}

	args := make([]string, 0)
	for i := 4; i < len(arrs); i++ {
		args = append(args, arrs[i])
	}

	c.User.CallTransactionSoft(arrs[1], arrs[2], args)

	loglogrus.Log.Infof("Dper: solidCallTransaction runs successfully!")
	return nil

}

func (c *CommandLine) softInvokeTransaction(arrs []string) error {

	if len(arrs) < 4 {
		loglogrus.Log.Warnf("Dper failed: solidInvokeTransaction unmatched arguments, Correct input format: invoke contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}
	if arrs[3] != "-args" {
		loglogrus.Log.Warnf("Dper failed: solidInvokeTransaction unmatched arguments, Correct input format: invoke contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}

	args := make([]string, 0)
	for i := 4; i < len(arrs); i++ {
		args = append(args, arrs[i])
	}

	c.User.InvokeTransactionSoft(arrs[1], arrs[2], args, c.txCheckMode)

	loglogrus.Log.Infof("Dper: softInvokeTransaction runs successfully, transaction has been upload blockChain!\n")
	return nil
}

func (c *CommandLine) softCallTransaction(arrs []string) error {

	if len(arrs) < 4 {
		loglogrus.Log.Warnf("Dper failed: solidCallTransaction unmatched arguments, Correct input format: invoke contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}
	if arrs[3] != "-args" {
		loglogrus.Log.Warnf("Dper failed: solidCallTransaction unmatched arguments, Correct input format: invoke contractAddr functionAddr -args arg1 arg2 arg3...\n")
		return fmt.Errorf("unmatched arguments")
	}

	args := make([]string, 0)
	for i := 4; i < len(arrs); i++ {
		args = append(args, arrs[i])
	}

	c.User.CallTransactionSoft(arrs[1], arrs[2], args)

	loglogrus.Log.Infof("Dper: softCallTransaction runs successfully!\n")
	return nil
}

package commandline

import (
	"dper/client"
	loglogrus "dper/loglogrus"
	"errors"
	"fmt"
	"os"
	"strings"
)

const (
	dpername = "DPER"
	version  = "1.1"
)

var (
	lineHead = ">>> " + dpername + " v" + version + " <<<"
)

type RoleType uint8

const (
	UnKnown RoleType = iota
	Booter
	Dper
)

type CommandLine struct {
	Role        RoleType
	User        *client.Client
	txCheckMode bool
}

func NewCommandLine(role RoleType, user *client.Client) *CommandLine {
	return &CommandLine{
		Role:        role,
		User:        user,
		txCheckMode: false,
	}
}

func (c *CommandLine) RunCommand(commandStr string) error {
	switch c.Role { //根据节点的类型采取不同指令执行策略
	case Dper:
		return c.runDperCommand(commandStr)
	case Booter:
		return c.runBooterCommand(commandStr)
	default:
		fmt.Printf("Start Stage: Unknown serve type , Please check whether the type is set for the current node (dper or booter)!\n")
		return fmt.Errorf("unknown serve type")
	}
}

func (c *CommandLine) runDperCommand(commandStr string) error {
	arrCommandStr := strings.Fields(commandStr) //以空白字符为间隔符,将输入指令进行分割
	if len(arrCommandStr) == 0 {
		loglogrus.Log.Warnf("Command is empty, please re-enter!\n")
		return errors.New("Command is empty, please re-enter!\n")
	}
	switch arrCommandStr[0] { //查看分割后的首部指令,采取不同执行策略
	case "listAccounts":
		// 打印本地已注册的所有账户
		accounts, err := c.User.AccountManager.Accounts()
		if err != nil {
			return err
		}
		c.printAccounts(accounts)
	case "createRemoteNewAccount":
		_, err := c.handleCreateRemoteNewAccounts(arrCommandStr)

		if err != nil {
			return err
		}
		fmt.Printf("Dper createRemoteNewAccount: Create new account successfully!\n")

	case "createLocalNewAccount":
		// 在本地创建一个新的账户，并切换到该新账户
		_, err := c.handleCreateLocalNewAccounts(arrCommandStr)

		if err != nil {
			return err
		}
		fmt.Printf("Dper createLocalNewAccount: Create new account successfully!\n")
	case "useAccount":
		accountAddr, err := c.handleUseAccount(arrCommandStr)
		if err != nil {
			return err
		}
		fmt.Printf("Dper useAccount: Change Account into (%x) successfully!\n", accountAddr)
	case "info", "Info", "INFO":
		c.printSelfInfo()
	case "txCheckMode":
		err := c.handleTxCheckMode(arrCommandStr)
		if err != nil {
			return err
		}
	case "solidInvoke":
		err := c.solidInvokeTransaction(arrCommandStr)
		if err != nil {
			return err
		}
	case "solidCall":
		err := c.solidCallTransaction(arrCommandStr)
		if err != nil {
			return err
		}

	case "invoke", "Invoke", "INVOKE", "softInvoke":
		err := c.softInvokeTransaction(arrCommandStr)
		if err != nil {
			return err
		}

	case "call", "Call", "CALL", "softCall":
		err := c.softCallTransaction(arrCommandStr)
		if err != nil {
			return err
		}

	case "viewNet":
		c.User.BackViewNetInfo()
	case "help":
		c.printUsages()

	case "tpbft":
		c.User.BackTPBFT()

	case "contract":
		c.User.BackContract()

	case "getBlockNum":
		c.User.GetBlockNum()

	default:
		loglogrus.Log.Warnf("Dper: Unknown command is input. Pint \"help\" to see all commands\n")
		return errors.New("Dper: Unknown command is input. Pint \"help\" to see all commands\n")
	}

	return nil
}

func (c *CommandLine) runBooterCommand(commandStr string) error {
	return nil
}

func (c *CommandLine) PrintLineHead() {
	fmt.Printf("\033[31;43m%s\033[0m $$ ", lineHead)
}

func (c *CommandLine) PrintError(err error) {
	errr := fmt.Errorf("dper Error: %v", err)
	fmt.Fprintln(os.Stderr, errr)
}

func (c *CommandLine) PrintByeBye() {
	byebye := `Dper is closed. 
Thanks for using Dper to manage P3-Chain ^_^ 
Hope to see you again.`
	fmt.Println(byebye)
}

func (c *CommandLine) Welcome() {

	copyRightInfo := "Copyright © 2022, P3-Chain Authors. All Rights Reserved.\nThis software is part of the project P3-Chain.\n"
	dpChainDescription := `P3-Chain is a consortium blockchain system that insists on supporting Byzantine fault-tolerance. It is an efficient, easy-use and safe blockchain platform, and will be well-known in the near future.
P3-Chain has good scalability and supports more nodes to run consensus method compared with current consortium blockchain system. This feature broadens the application scenarios where user is node of P3-Chain.
P3-Chain builds a native blockchain platform system with sharding management and support shards for collaborative interaction, which avoids the performance and security degradation caused by chain-cross facilities.
`

	bannerDpchainInfo := `
===========================================================
____ _____        ____ _   _    _    ___ _   _ 
|  _ \___ /       / ___| | | |  / \  |_ _| \ | |
| |_) ||_ \ _____| |   | |_| | / _ \  | ||  \| |
|  __/___) |_____| |___|  _  |/ ___ \ | || |\  |
|_|  |____/       \____|_| |_/_/   \_\___|_| \_|
                                                                                                                         
===========================================================
`
	dperDescription := `Welcome to use Dper.
Dper is a client terminal providing users with the basic way to construct and manage the P3-Chain.
Before using Dper to construct a P3-Chain, user should config the settings which is in path './settings/dperConfig.json'. P3-Chain provides users several ways to construct and initialize it, however,  the Dper now only provides users with the basic state-construct-start way. 
Version Features:
1. Support the three-stage (state-construct-start) P3-Chain construction method.
2. Support booter mode, and the default config path is in './settings/booterConfig.json'.
3. Support simple transaction invoke/call.
`
	bannerDperInfo := `
===========================================================
                                        __________
  _____                                / ___  ___ \
 |  __ \                              / / @ \/ @ \ \
 | |  | |  _ __     ___   _ __        \ \___/\___/ /\
 | |  | | | '_ \   / _ \ | '__|        \____\/____/||
 | |__| | | |_) | |  __/ | |           /     /\\\\\//
 |_____/  | .__/   \___| |_|           |     |\\\\\\
          | |                          \      \\\\\\
          |_|                           \______/\\\\
                                         _||_||_
===========================================================
`
	dpchainInfo := copyRightInfo + bannerDpchainInfo + dpChainDescription
	fmt.Print(dpchainInfo)
	dperInfo := copyRightInfo + bannerDperInfo + dperDescription
	fmt.Println()
	fmt.Print(dperInfo)
	startInfo := fmt.Sprintf("Client %s v%s starts!\n", dpername, version)
	fmt.Print(startInfo)
}

func (c *CommandLine) printByeBye() {
	byebye := `Dper is closed. 
Thanks for using Dper to manage P3-Chain ^_^ 
Hope to see you again.`
	fmt.Println(byebye)
}

func (c *CommandLine) printUsages() string {
	switch c.Role {
	case Dper:
		commandsInfo := `Dper is a client terminal providing users with the basic way to construct and manage the P3-Chain.

To initialize the dper:
  init             Load the config, and initialize the dper.
  rpc			   start rpc service to run contract.

To join the P3-Chain, please go through the three-stage initialization:
  state            State the node self to the P3-Chain network (dpnet).
  construct        Use the received node state information to construct dpnet.
  start            Start the dper client after the construction of dpnet.

Common Commands:
  help             Display all the commands and so the usages.
  exit,quit        Close the dper client.
  listAccounts     List out all the accounts stored.
  info             Print out the current state of Dper.
  viewNet          Pint out the information about the dpnet the dper known. 
  createNewAccount Create a new account and set it as the default user account.
    usage:         createNewAccount 
                     -- Create an account with no password.
                   createNewAccount -p yourPassword		
                     -- Create an account with yourPassword. 				   
  useAccount       Use account with the password input and set it as default account.
    usage:         useAccount yourAccountAddress 
                     -- use yourAccountAddress to load user.
                   useAccount yourAccountAddress -p yourPassword
                     -- use yourAccountAddress and yourPassword to load user.
  txCheckMode      Set the transaction check mode (default is false). When this mode is on, invoke (both soft and solid) will wait no more than 10s to back the transaction results.
    usage:         txCheckMode on
                     -- set transaction check mode on
                   txCheckMode off
                     -- set transaction check mode off
  invoke           Use contract name and function name to invoke a transaction and broadcast it to the P3-Chain.
    usage:         invoke contractName functionName -args arg1 arg2 ...
                     -- contractName and functionName would be converted into address.
  call             Use contract name and function name to invoke a transaction locally and print the results got.
    usage:         call contractName functionName -args arg1 arg2 ...
                     -- contractName and functionName would be converted into address.
  solidInvoke      Use contract address and function address to invoke a transaction and broadcast it to the P3-Chain.
    usage:         solidInvoke contractAddr functionAddr -args arg1 arg2 ...
                     -- should specify the contract and function 20-bytes address.
  solidCall        Use contract address and function address to invoke a transaction locally and print the results got.
    usage:         solidCall contractAddr functionAddr -args arg1 arg2 ...
                     -- should specify the contract and function 20-bytes address.

Mode Change:
  beBooter         Change client mode from Dper mode to booter. Should be used before initiating Dper.
`
		fmt.Print(commandsInfo)
		return commandsInfo
	case Booter:
		commandsInfo := `Dper is a client terminal providing users with the basic way to construct and manage the P3-Chain.

Now Dper client has been changed to booter mode. 

To initialize the booter:
  init             Load the config, and initialize the booter.

To help nodes to construct P3-Chain and run upper-level consensus, booter also should go through the three-stage initialization:
  state            State the booter self to the P3-Chain network (dpnet).
  construct        Use the received node state information to construct dpnet.
  start            Start providing the upper block ordering service after the construction of dpnet.
  
Useful Commands:
  viewNet          Pint out the information about the dpnet the booter known.
  exit,quit        Close the booter (of say dper) client.
  saveurl          Save the booter self url which could be copied to other dper used as bootstrap node.
`
		fmt.Print(commandsInfo)
		return commandsInfo
	default:
		fmt.Println("Unknown serve type is got!")
		return ""
	}
}

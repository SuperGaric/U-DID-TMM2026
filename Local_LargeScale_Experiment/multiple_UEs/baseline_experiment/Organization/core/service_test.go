package core

import (
	"testing"
)

func TestService(t *testing.T) {
	keyStorePathForTest := "./keyStore"
	srv := NewDIDService(keyStorePathForTest)
	user := srv.CreateLocalUser("")

	args := make([][]byte, 0)
	tx := srv.BuildTransaction(user, "SampleContract", "SampleFunction", args)
	bitCurrent := srv.CompressTransaction(tx)
	t.Logf("The result is: %x", bitCurrent)

}

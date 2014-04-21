package main

import (
  "crypto/sha256"
  "encoding/hex"
  "fmt"
)

func main() {
  hash := sha256.New()
  hash.Write([]byte("username,12345,999999"))
  md := hash.Sum(nil)
  mdStr := hex.EncodeToString(md)
  fmt.Printf(mdStr)
}

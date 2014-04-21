package main

import (
  "crypto/sha256"
  "encoding/hex"
  "flag"
  "fmt"
)

var (
  username = flag.String("username", "username", "What is the username to crack?")
  salt     = flag.String("salt", "999999", "What is the salt to crack?")
)

func init() {
  flag.Parse()
}

func main() {
  hash := sha256.New()
  hash.Write([]byte(*username + ",12345," + *salt))
  md := hash.Sum(nil)
  mdStr := hex.EncodeToString(md)
  fmt.Printf(mdStr)
}

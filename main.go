package main

import (
  "crypto/sha256"
  "encoding/hex"
  "flag"
  "fmt"
  "runtime"
)

var (
  username = flag.String("username", "ristenpart", "What is the username to crack?")
  salt     = flag.String("salt", "134153169", "What is the salt to crack?")
  hash     = flag.String("hash", "37448ba7de7f5b4396697edaeddcd7bc840964e6ce82016915b830a91d69eb2f", "What is the hash to crack?")
)

func init() {
  flag.Parse()

  // Set runtime GOMAXPROCS
  runtime.GOMAXPROCS(runtime.NumCPU())
}

func main() {
  sha := sha256.New()
  sha.Write([]byte(*username + ",12345," + *salt))
  test := hex.EncodeToString(sha.Sum(nil))
  fmt.Println(test)
}

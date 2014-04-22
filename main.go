package main

import (
  "crypto/sha256"
  "encoding/hex"
  "flag"
  "fmt"
  "runtime"
  "time"
)

var (
  username = flag.String("username", "ristenpart", "What is the username to crack?")
  salt     = flag.String("salt", "134153169", "What is the salt to crack?")
  hash     = flag.String("hash", "37448ba7de7f5b4396697edaeddcd7bc840964e6ce82016915b830a91d69eb2f", "What is the hash to crack?")
  size     = flag.Int("size", 1<<15, "What is the batch size for each worker?")
  max      = flag.Int("max", 1<<31, "What is the max integer password to look for?")
)

func init() {
  flag.Parse()

  // Set runtime GOMAXPROCS
  runtime.GOMAXPROCS(runtime.NumCPU())
}

func main() {
  batch := make(chan int)

  for i := 0; i < runtime.NumCPU(); i++ {
    go func() {
      for batchIndex := range batch {
        for i := batchIndex; i < (int(batchIndex+1) * (*size)); i++ {
          sha := sha256.New()
          sha.Write([]byte(fmt.Sprintf("%s,%d,%s", *username, i, *salt)))
          test := hex.EncodeToString(sha.Sum(nil))
          if test == *hash {
            fmt.Printf("The integer password: %d\n", i)
            fmt.Printf("Produces this hash: %s\n", test)
            close(batch)
          }
        }
      }
    }()
  }

  defer func() { recover() }()

  timeStart := time.Now()
  batchStart := 0
  for i := 0; i < *max / *size; i++ {
    batch <- i
    if timeEnd := time.Now(); timeEnd.Sub(timeStart) > time.Second {
      fmt.Printf("Hashing at %d/sec\n", int(i-batchStart)*(*size))
      batchStart = i
      timeStart = time.Now()
    }
  }
}

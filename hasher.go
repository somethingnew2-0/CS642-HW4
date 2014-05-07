package main

import (
  "crypto/sha256"
  "encoding/hex"
  "flag"
  "fmt"
  "runtime"
  "sync/atomic"
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
  ticker := time.NewTicker(time.Second)
  var ops uint64 = 0

  go func() {
    lastOps := atomic.LoadUint64(&ops)
    for _ = range ticker.C {
      recentOps := atomic.LoadUint64(&ops)
      fmt.Printf("Hashing at %d hashes/sec\n", recentOps-lastOps)
      lastOps = recentOps
    }
  }()

  batch := make(chan int)

  for i := 0; i < runtime.NumCPU(); i++ {
    go func() {
      for batchIndex := range batch {
        for i := batchIndex; i < (int(batchIndex+1) * (*size)); i++ {
          sha := sha256.New()
          sha.Write([]byte(fmt.Sprintf("%s,%d,%s", *username, i, *salt)))
          test := hex.EncodeToString(sha.Sum(nil))
          atomic.AddUint64(&ops, 1)
          if test == *hash {
            fmt.Println("The integer password:", i)
            fmt.Println("Produces this hash:", test)
            ticker.Stop()
            close(batch)
          }
        }
        runtime.Gosched()
      }
    }()
  }

  defer func() { recover() }()

  for i := 0; i < *max / *size; i++ {
    batch <- i
  }
}

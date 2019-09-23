# NATS Client

## Requirements

You should `go get` gnatsd first. This is nats server binary file.

```sh
go get github.com/nats-io/gnatsd
```

After this, you will find `gnatsd` file in your `$GOPATH/bin` folder. Just execute

```sh
cd $GOPATH/bin
./gnatsd
```

to start the server.

In addition, you can find gnatsd porject's source code in `$GOPATH/src/github.com/gnatsd`.

## Client project

- [Golang](./golang/README.md)
- [Python](./python/README.md)
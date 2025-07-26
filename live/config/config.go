package config

import (
	"fmt"
	"time"
)

var DatabaseFilePath = "data/owncast.db"

var LogDirectory = "./data/logs"

var TempDir = "./data/tmp"

var EnableDebugFeatures = false

var VersionNumber = StaticVersionNumber

var WebServerPort = 8080

var WebServerIP = "0.0.0.0"

var InternalHLSListenerPort = "8927"

var GitCommit = ""

var BuildPlatform = "dev"

var EnableAutoUpdate = false

var TemporaryStreamKey = ""

func GetCommit() string {
	if GitCommit == "" {
		GitCommit = time.Now().Format("20060102")
	}

	return GitCommit
}

var DefaultForbiddenUsernames = []string{
	"owncast", "operator", "admin", "system",
}

const MaxSocketPayloadSize = 2048

func GetReleaseString() string {
	versionNumber := VersionNumber
	buildPlatform := BuildPlatform
	gitCommit := GetCommit()

	return fmt.Sprintf("Owncast v%s-%s (%s)", versionNumber, buildPlatform, gitCommit)
}

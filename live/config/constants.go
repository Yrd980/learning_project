package config

import "path/filepath"

const (
	StaticVersionNumber = "0.2.3"

	FfmpegSuggestedVersion = "v4.1.5"

	DataDirectory = "data"

	EmojiDir = "/img/emoji/"

	MaxUserColor = 7

	MaxChatDisplayNameLength = 30
)

var (
	BackupDirectory = filepath.Join(DataDirectory, "backup")

	HLSStoragePath = filepath.Join(DataDirectory, "hls")

	CustomEmojiPath = filepath.Join(DataDirectory, "emoji")

	PublicFilesPath = filepath.Join(DataDirectory, "public")
)

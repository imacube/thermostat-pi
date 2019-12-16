# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Visioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed
- A function that was used by one method to move variables into a bytearray. This overly complicated things.

## 0.5.0 - 2019-11-27

### Added
- Script to restart `send-temp.service` if the underlying script fails. The call that fails
  according to the stacktrace is one handled by Digi with no option to set a timeout that
  I found on my initial search.

## 0.4.0 - 2019-09-26
Merged everything back into develop and master. Tagged it. This includes initial PyCharm files.

### Added
- Initial version for `CHANGELOG.md`




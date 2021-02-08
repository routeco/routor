# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

* download multiple regions into a single file

## [0.3.0] - 2021-02-05

### Added

* Edge/Node will be populated with all tags/attributes defined (use `getattr()` with a default value to retrieve them)
* Added Optional bearing/grade to models

## [0.2.1] - 2021-02-05

### Fixed

* Download did not work, since the internal click API does not return a proper object

## [0.2.0] - 2021-02-05

### Added

* ability to include more edge/node tags into the graph
* automatically tag nodes part of a roundabout as junction=roundabout
* add elevation to nodes when a Google API key is provided
* add edge grades when a Google API key is provided

### Changed

* dropped unused oneway conversion

## [0.1.0] - 2020-01-18

### Added

* basic routing CLI
* basic API

[Unreleased]: https://github.com/escaped/routor/compare/0.3.0...HEAD
[0.3.0]: https://github.com/escaped/routor/compare/0.2.1...0.3.0
[0.2.1]: https://github.com/escaped/routor/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/escaped/routor/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/escaped/routor/tree/0.1.0

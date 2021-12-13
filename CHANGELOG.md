# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.0] - 2021-12-13

### Changed

* update all dependencies and be compatible with more versions

## [0.6.0] - 2021-11-01


### Changed

* compatibility with osmnx 1.1.x

## [0.5.1] - 2021-06-15

### Changed

* extended internal API to be able to use different functions to download a graph from OSM

## [0.5.0] - 2021-03-29

### Changed

* travel time calculation can now be customized using a weight function

## [0.4.0] - 2021-02-09

### Added

* download multiple regions into a single file
* plugin mechanism 

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

[Unreleased]: https://github.com/escaped/routor/compare/0.7.0...HEAD
[0.7.0]: https://github.com/escaped/routor/compare/0.6.0...0.7.0
[0.6.0]: https://github.com/escaped/routor/compare/0.5.1...0.6.0
[0.5.1]: https://github.com/escaped/routor/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/escaped/routor/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/escaped/routor/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/escaped/routor/compare/0.2.1...0.3.0
[0.2.1]: https://github.com/escaped/routor/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/escaped/routor/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/escaped/routor/tree/0.1.0

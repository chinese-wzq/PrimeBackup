from typing import NamedTuple, List, Union, Iterator

from mcdreforged.api.all import *

from prime_backup.db import schema
from prime_backup.types.file_info import FileInfo


class ExportFailure(NamedTuple):
	file: FileInfo
	error: Exception


class ExportFailures:
	def __init__(self, fail_soft: bool):
		self.__fail_soft = fail_soft
		self.failures: List[ExportFailure] = []

	def add_or_raise(self, file: Union[FileInfo, schema.File], error: Exception):
		if self.__fail_soft:
			if isinstance(file, schema.File):
				file = FileInfo.of(file)
			self.failures.append(ExportFailure(file, error))
		else:
			raise error

	def __len__(self) -> int:
		return len(self.failures)

	def __iter__(self) -> Iterator[ExportFailure]:
		return self.failures.__iter__()

	def to_lines(self) -> List[RTextBase]:
		from prime_backup.mcdr.text_components import TextColors
		result = []
		for failure in self.failures:
			result.append(RTextBase.format(
				'{} mode={}: ({}) {}',
				RText(failure.file.path, TextColors.file),
				oct(failure.file.mode),
				type(failure.error).__name__,
				str(failure.error),
			))
		return result

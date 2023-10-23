class PySipebiDiagnosticsError:
	ErrorCode = '[Kode]'
	ParagraphNo = 0
	ElementNo = 0
	OriginalElement = ''
	CorrectedElement = ''
	OriginalParagraphOffset = 0
	PositionOffset = 0
	CorrectedCharPosition = 0
	IsAmbiguous = False

	def SimpleDisplay(self):
		return self.ErrorCode + ' ' + self.OriginalElement + ' -> ' + self.CorrectedElement

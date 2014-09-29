from oonib.collector import handlers

reportAPI = [
    (r"/report/([a-zA-Z0-9_\-]+)/close", handlers.CloseReportHandlerFile),
    (r"/report/([a-zA-Z0-9_\-]+)", handlers.UpdateReportHandlerFile),
    (r"/report", handlers.NewReportHandlerFile),
    (r"/pcap", handlers.PCAPReportHandler),
]

policyAPI = [
    (r"/policy/nettest", handlers.NetTestPolicyHandler),
    (r"/policy/input", handlers.InputPolicyHandler),
]

inputAPI = [
    (r"/input", handlers.InputListHandler),
    (r"/input/([a-f0-9]{64})", handlers.InputDescHandler),
    (r"/input/([a-f0-9]{64})/file$", handlers.InputFileHandler)
]

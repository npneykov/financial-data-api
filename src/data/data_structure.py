import jsonpickle


class FinancialData:
    def __init__(
        self,
        id,
        start_date,
        end_date,
        timeframe,
        fiscal_period,
        fiscal_year,
        cik,
        sic,
        tickers,
        company_name,
    ):
        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.timeframe = timeframe
        self.fiscal_period = fiscal_period
        self.fiscal_year = fiscal_year
        self.cik = cik
        self.sic = sic
        self.tickers = tickers
        self.company_name = company_name

    def to_json(self):
        return jsonpickle.encode(self)

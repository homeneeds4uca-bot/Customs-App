"""
Tariff rates model for storing CBSA tariff schedule data
"""
from datetime import datetime, date
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Date,
    TIMESTAMP,
    Text,
    DECIMAL,
)

from backend.core.database import Base


class TariffRate(Base):
    """Tariff rates model for CBSA tariff schedule"""

    __tablename__ = "tariff_rates"

    # Primary key (HS code)
    hs_code = Column(String(10), primary_key=True)

    # HS code breakdown
    chapter = Column(String(2), index=True)  # First 2 digits
    heading = Column(String(4), index=True)  # First 4 digits
    subheading = Column(String(6))  # First 6 digits

    # Descriptions
    description_en = Column(Text, nullable=False)
    description_fr = Column(Text)

    # Duty rates (as decimal, e.g., 0.06 = 6%)
    mfn_rate = Column(DECIMAL(5, 4))  # Most Favored Nation
    usmca_rate = Column(DECIMAL(5, 4))  # United States-Mexico-Canada Agreement
    cptpp_rate = Column(DECIMAL(5, 4))  # Comprehensive and Progressive Agreement for Trans-Pacific Partnership
    ceta_rate = Column(DECIMAL(5, 4))  # Canada-European Union Comprehensive Economic and Trade Agreement
    gpt_rate = Column(DECIMAL(5, 4))  # General Preferential Tariff
    ldct_rate = Column(DECIMAL(5, 4))  # Least Developed Country Tariff

    # Flags
    gst_applicable = Column(Boolean, default=True)
    excise_applicable = Column(Boolean, default=False)

    # Unit of measure
    unit_of_measure = Column(String(50))

    # Effective date
    effective_date = Column(Date)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TariffRate(hs_code={self.hs_code}, mfn_rate={self.mfn_rate})>"

    def get_rate_for_country(self, country_code: str) -> float:
        """
        Get the applicable duty rate for a given country of origin.

        Args:
            country_code: ISO 2-letter country code

        Returns:
            Applicable duty rate as decimal
        """
        # Preferential rates by country/trade agreement
        preferential_rates = {
            "US": self.usmca_rate,  # United States - USMCA
            "MX": self.usmca_rate,  # Mexico - USMCA
            # Add more countries as needed
        }

        rate = preferential_rates.get(country_code)
        if rate is not None:
            return float(rate)

        # Default to MFN rate
        return float(self.mfn_rate) if self.mfn_rate is not None else 0.0

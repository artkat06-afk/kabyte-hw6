import pandera.pandas as pa
from pandera import Column, Check, DataFrameSchema

listing_schema = DataFrameSchema(
    columns={
        "id": Column(int, Check.greater_than(0), nullable=False),
        "price": Column(float, Check.in_range(100000, 100000000), nullable=False),
        "area": Column(float, Check.in_range(10, 500), nullable=False),
        "floor": Column(int, Check.greater_than(0), nullable=False),
        "total_floors": Column(int, Check.greater_than(0), nullable=False),
        "address": Column(str, Check.str_length(min_value=5), nullable=False),
        "photo_s3_uris": Column(object, nullable=True),
    },
    checks=[
        Check(lambda df: df["floor"] <= df["total_floors"], name="floor_lte_total")
    ],
    strict=False,
    coerce=True,
)
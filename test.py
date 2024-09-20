from pyspark.sql.types import (
    StructType, StructField,
    StringType, IntegerType, FloatType, DoubleType,
    BooleanType, DateType, TimestampType, LongType, ShortType,
    ArrayType, MapType
)
import pandas as pd
import numpy as np

def pandas_to_spark(pandas_df):
    """
    Converts a pandas DataFrame to a PySpark DataFrame, handling data type
    inference and merging issues.

    Parameters:
    - pandas_df: The pandas DataFrame to convert.

    Returns:
    - A PySpark DataFrame.
    """
    from pyspark.sql import SparkSession

    # Get the active SparkSession
    spark = SparkSession.getActiveSession()
    if spark is None:
        raise RuntimeError("No active SparkSession found. Please initialize a SparkSession before calling this function.")

    # Map pandas dtypes to PySpark types
    dtype_map = {
        'int64': LongType(),
        'int32': IntegerType(),
        'int16': ShortType(),
        'float64': DoubleType(),
        'float32': FloatType(),
        'bool': BooleanType(),
        'datetime64[ns]': TimestampType(),
        'object': StringType(),
        'category': StringType(),
    }

    def get_struct_type(pdf):
        fields = []
        for column_name, dtype in pdf.dtypes.items():
            if str(dtype) in dtype_map:
                data_type = dtype_map[str(dtype)]
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                data_type = TimestampType()
            elif pd.api.types.is_bool_dtype(dtype):
                data_type = BooleanType()
            elif pd.api.types.is_integer_dtype(dtype):
                data_type = LongType()
            elif pd.api.types.is_float_dtype(dtype):
                data_type = DoubleType()
            elif pd.api.types.is_categorical_dtype(dtype):
                data_type = StringType()
            elif pd.api.types.is_string_dtype(dtype):
                data_type = StringType()
            elif pd.api.types.is_object_dtype(dtype):
                sample_value = pdf[column_name].dropna().iloc[0] if not pdf[column_name].dropna().empty else None
                if isinstance(sample_value, list):
                    data_type = ArrayType(StringType())
                elif isinstance(sample_value, dict):
                    data_type = MapType(StringType(), StringType())
                else:
                    data_type = StringType()
            else:
                data_type = StringType()  # Default to StringType if unknown
            fields.append(StructField(column_name, data_type, True))
        return StructType(fields)

    # Handle empty DataFrame
    if pandas_df.empty:
        schema = get_struct_type(pandas_df)
        spark_df = spark.createDataFrame([], schema)
    else:
        schema = get_struct_type(pandas_df)
        spark_df = spark.createDataFrame(pandas_df, schema=schema)

    return spark_df
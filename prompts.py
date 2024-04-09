import streamlit as st

Tables=[{'QUALIFIED_TABLE_NAME' : "FINANCEDWH.FDWH.FINANCIALS",
'METADATA_QUERY' : "SELECT REPORTING_PERIOD,CLIENT_ID,CHANNEL_ID,REGION_ID,FUND_ID,CURRENCY,SALES,ASSETS,REVENUE,COMMENTS FROM FINANCEDWH.FDWH.FINANCIALS;",
'TABLE_DESCRIPTION' : "This table is about Financials. This stores information about Revenue , Sales and Assets. Revenue is known as earnings."},
{'QUALIFIED_TABLE_NAME' : "FINANCEDWH.FDWH.CHANNEL",
'METADATA_QUERY' : "SELECT CHANNEL_ID,CHANNEL_NAME,COMMENTS FROM FINANCEDWH.FDWH.CHANNEL;",
'TABLE_DESCRIPTION' : "This table is about Channels."},
{'QUALIFIED_TABLE_NAME' : "FINANCEDWH.FDWH.CLIENT",
'METADATA_QUERY' : "SELECT CLIENT_ID,CLIENT_NAME,COMMENTS FROM FINANCEDWH.FDWH.CLIENT;",
'TABLE_DESCRIPTION' : "This table is about Client."},
{'QUALIFIED_TABLE_NAME' : "FINANCEDWH.FDWH.FUND",
'METADATA_QUERY' : "SELECT FUND_ID,FUND_NAME,COMMENTS FROM FINANCEDWH.FDWH.FUND;",
'TABLE_DESCRIPTION' : "This table is about Funds."},
{'QUALIFIED_TABLE_NAME' : "FINANCEDWH.FDWH.REGION",
'METADATA_QUERY' : "SELECT REGION_ID,REGION_NAME,COMMENTS FROM FINANCEDWH.FDWH.REGION;",
'TABLE_DESCRIPTION' : "This table is about REGION."},
{'QUALIFIED_TABLE_NAME' : "FINANCEDWH.FDWH.PROFITABILITY",
'METADATA_QUERY' : "SELECT MANAGEMENT_FEES, ADMIN_FEES, THIRD_PARTY_FUND_REVENUE, ASSET_BASED_DISTRIBUTION_FEES, FUND_EXPENSE_WRITE_OFFS, TOTAL_ASSET_BASED_REVENUE, PERFORMANCE_FEES, OTHER_DISTRIBUTION_FEES, OTHER_REVENUE, TOTAL_REVENUE, STAFF_COSTS, BONUS_PSP, PROFESSIONAL_AND_OUTSOURCED_FEES, TRAVEL_AND_ENTERTAINMENT, OTHER_DIRECT_COSTS, MARKETING_COSTS, OTHER, ADVISORY_FEES, CENTRAL_ADJS, TOTAL_COSTS_AUG22_FX, FX_IMPACT, TOTAL_COSTS, PROFIT_LOSS, MARGIN, NET_EARNINGS, REPORTING_PERIOD FROM FINANCEDWH.FDWH.PROFITABILITY;",
'TABLE_DESCRIPTION' : "This table is about PROFITABILITY of CFP data."}
]

# 93 token --> 4100
GEN_SQL = """
You will be acting as an AI expert named FIL SnowBot.
Your goal is to give correct information with sql query.
Please return fund name, channel name , region name and client name when user ask about fund, channel, regions and client respectively.

{context}
"""

#@st.cache_data(show_spinner=False)
def get_table_context(table_name: str, table_description: str, metadata_query: str = None):
    table = table_name.split(".")
    conn = st.experimental_connection("snowpark")
    columns = conn.query(f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
        """,
    )
    #st.text(type(columns))
    #st.text(columns)
    
    columns = "\n".join(
        [
            f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
            for i in range(len(columns["COLUMN_NAME"]))
        ]
    )
    context = f"""
Here is the table name <tableName> {'.'.join(table)} </tableName>

<tableDescription>{table_description}</tableDescription>

Here are the columns of the {'.'.join(table)}

<columns>\n\n{columns}\n\n</columns>
    """
    if metadata_query:
        metadata = conn.query(metadata_query)
        #st.text(metadata)
        '''metadata = "\n".join(
            [
                f"- **{metadata['REPORTING_PERIOD'][i]}**: {metadata['COMMENTS'][i]}"
                for i in range(len(metadata["REPORTING_PERIOD"]))
            ]
        )'''
        context = context + f"\n\nAvailable variables by REPORTING_PERIOD:\n\n{metadata}"
    return context

def get_system_prompt():
    st.header("System prompt for FIL SnowBot")
    final=''
    for table_info in Tables:
        
        table_context = get_table_context(
            table_name=table_info["QUALIFIED_TABLE_NAME"],
            table_description=table_info["TABLE_DESCRIPTION"],
            metadata_query=table_info["METADATA_QUERY"]
        )
        final+=GEN_SQL.format(context=table_context)


    return final



'''# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for FIL SnowBot")
    for table_info in Tables:
        st.markdown(get_system_prompt(table_info))'''
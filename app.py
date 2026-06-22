import streamlit as st
import pandas as pd

st.set_page_config(
    page_title=" Skycity Restuarant Growth Analysis",
    layout="wide"
)
df=pd.read_csv("restaurant_final.csv")
st.title("Skycity Restaurant Growth Analysis Dashboard")
st.write("Interactive dashboard for restaurant performance,"
         "growth potential and strategic recommendations")
# Sidebar filters......
st.sidebar.header("Restaurant Filters")
cuisine_filter=st.sidebar.multiselect("Select Cuisine",
                                    df['CuisineType'].unique())
segment_filter=st.sidebar.multiselect("Select Segment",df['Segment'].unique())

region_filter=st.sidebar.multiselect("Select Subregion",df['Subregion'].unique())

filtered_df=df.copy()
if cuisine_filter:
    filtered_df=filtered_df[
        filtered_df['CuisineType'].isin(cuisine_filter)
    ]

if segment_filter:
    filtered_df=filtered_df[
        filtered_df['Segment'].isin(segment_filter)
    ]

if region_filter:
    filtered_df=filtered_df[
        filtered_df['Subregion'].isin(region_filter)
    ]
st.divider()



# KPI section......
st.subheader("Business Performance Overview")
col1,col2,col3,col4=st.columns(4)
with col1:
    st.metric("Total Restaurants",
              len(filtered_df))
with col2:
    st.metric("Average Revenue",
              f"${filtered_df['TotalRevenue'].mean():,.0f}")
with col3:
    st.metric("Average Profit",
              f"${filtered_df['TotalProfit'].mean():,.0f}")
with col4:
    st.metric("High Potential Restaurants",
              len(filtered_df[filtered_df['GPI_Category']=="High Potential"]))
              


# cluster distribution chart......
import plotly.express as px
st.subheader("Restaurant Distribution Across Clusters")
cluster_count=(
    filtered_df['Cluster'].value_counts().reset_index())
cluster_count.columns=['Cluster','Restaurant_Count']
fig=px.bar(cluster_count,x='Cluster',y='Restaurant_Count',text='Restaurant_Count',title=
           'Number of Restaurants in Each Cluster')
st.plotly_chart(fig,use_container_width=True)
st.divider()

# revenue vs profit by cluster......
st.subheader("Revenue vs Profit Performance by Cluster")
fig=px.scatter(filtered_df,x="TotalRevenue",y="TotalProfit",color="Cluster_Label", 
hover_data=['CuisineType','Segment','Subregion'],title="Restaurant Revenue vs Profit by Cluster")
fig.update_layout(xaxis_title="Total Revenue",yaxis_title="Total Profit")
st.plotly_chart(fig,use_container_width=True)
st.divider()

# GPI Category distribution chart......
st.subheader("Growth Potential Distribution")
gpi_count=(filtered_df['GPI_Category'].value_counts().reset_index())
gpi_count.columns=['GPI_Category','Restaurant_Count']
fig=px.bar(gpi_count,x='GPI_Category',y='Restaurant_Count',text='Restaurant_Count',
           title='Restaurant by Growth Potential Category')
st.plotly_chart(fig,use_container_width=True)
st.divider()

# cluster performance......
st.subheader("Cluster Performance Comparison")
cluster_summary=(
    filtered_df.groupby('Cluster_Label')
    [['TotalRevenue','TotalProfit','ProfitMargin']].mean().reset_index().round(2))
cluster_colors={'Growth Leaders':'green','Stable Local Performers':'blue',
                'Aggregator-dependent Low Margin':'red',
                'Scalable Self-delivery Leaders':'purple'}
fig =px.bar(cluster_summary,x='Cluster_Label',y='TotalProfit',text=cluster_summary['TotalProfit'].round(2),
            color='Cluster_Label',color_discrete_map=cluster_colors,title='Average Profit Performance by Cluster')
fig.update_layout(xaxis_title="Cluster",yaxis_title='Average Profit')
st.plotly_chart(fig,use_container_width=True)
st.divider()


# strategic recommendation panel......
st.subheader("Strategic Recommendation Overview")
recommendation_summary=(filtered_df['Recommendation'].value_counts().reset_index())
recommendation_summary.columns=['Recommendation','Restaurant_Count']
color_map={'Expand':'green','Optimize':'red','Hold/Stabilize':'blue'}
fig=px.bar(recommendation_summary,x='Recommendation',y='Restaurant_Count',
           text='Restaurant_Count',color='Recommendation',color_discrete_map=color_map,title='Recommended Business Actions')

st.plotly_chart(fig,use_container_width=True)
st.divider()

# restaurant strategy details......
st.subheader("Restaurant-Level Strategic Actions")
strategy_table = filtered_df[['Cluster_Label','Recommendation','GPI_Category','TotalRevenue',
                              'TotalProfit']].head(20)

# format currency  for dispaly
strategy_table['TotalRevenue']=strategy_table['TotalRevenue'].apply(lambda x:f"${x:,.0f}")
strategy_table['TotalProfit']=strategy_table['TotalProfit'].apply(lambda x:f"${x:,.0f}")

st.dataframe(strategy_table)




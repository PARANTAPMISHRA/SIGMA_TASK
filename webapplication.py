import streamlit as st
import pandas as pd
import datetime 
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
st.set_page_config(layout='wide',page_title='EDA',page_icon='bar_chart') 
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file is not None:
    

    df=pd.read_csv(uploaded_file)
        
     
    dataset_size = df.shape[0]
    num_features = df.shape[1]
    num_nan_values = df.isna().sum().sum()
    
    
    st.title('Dataset Overview')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Dataset Size", value=dataset_size)
    
    
    with col2:
        st.metric(label="Number of Features", value=num_features)
    
    
    with col3:
        st.metric(label="Number of NaN Values", value=num_nan_values)
    
    
    col4,col5,col6=st.columns([1,1,1])
    
    
    with col4:
        
        brand_popularity = df['brand_name'].value_counts().head()
        
        fig7 = px.pie(names=brand_popularity.index, values=brand_popularity.values, 
                    labels={'names': 'Brand Name', 'values': 'Number of Products'}, 
                    title='Brand Popularity',hole=0.5)
        fig7.update_layout(width=440)
        st.plotly_chart(fig7)
    
    
    with col5:
    
        top_n_brands = 10
    
        
        brand_counts = df['brand_name'].value_counts().head(top_n_brands)
    
        
        top_brands_df = df[df['brand_name'].isin(brand_counts.index)]
        top_brands_stats = pd.DataFrame({'Name': brand_counts.index,'Count': brand_counts.values})
        top_brands_stats.sort_values(by='Name',ascending=True,inplace=True)
    
        brand_count=top_brands_stats[['Name','Count']]
        brand_count=top_brands_stats[['Name','Count']]
    
        
        top_brands = brand_count['Name']  
    
        
        filtered_df = df[df['brand_name'].isin(top_brands)]
        
        average_prices = filtered_df.groupby('brand_name')[['price_usd', 'seller_price', 'seller_earning', 'buyers_fees']].mean()
    
        
        fig14 = px.bar(average_prices,title='Average Prices of Top 10 Brands', labels={'x': 'Brand', 'y': 'Average Price','variable':'Price Type'})
    
        
        fig14.update_layout(xaxis_tickangle=-45, legend_title_text='Price Type')
        fig14.update_layout(width=460)
        st.plotly_chart(fig14)
    
    
    with col6:
        
        average_ratings = filtered_df.groupby('brand_name')['product_like_count'].mean()
    
        
        average_ratings = average_ratings.reindex(top_brands)
    
        fig12=px.bar(x=average_ratings.index,y=average_ratings.values,color=average_ratings.values,color_continuous_scale='viridis',title='Average Rating of Top 10 Brands')
        fig12.update_layout(xaxis_tickangle=-90)
        fig12.add_trace(go.Line(x=average_ratings.index,y=average_ratings.values,name='Trend Line',line=dict(color='royalblue')))
        fig12.update_layout(width=470)
        st.plotly_chart(fig12)
    
    
    col14,col15=st.columns(2)
    
    
    with col14:
        brand = df.groupby('seller_country')['brand_name'].agg(lambda x: x.value_counts().idxmax()).reset_index()
        fig = px.choropleth(
                brand,
                locations='seller_country',
                locationmode='country names',
                color='brand_name',
                title='Most Common Brands by Country',
                color_continuous_scale=px.colors.sequential.Plasma,
            )
        fig.update_layout(width=600)
        st.plotly_chart(fig)
    
    
    with col15:
        product_type = df.groupby('seller_country')['product_type'].agg(lambda x: x.value_counts().idxmax()).reset_index()
        fig = px.choropleth(
            product_type,
            locations='seller_country',
            locationmode='country names',
            color='product_type',
            title='Most Common Product by Country',
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig.update_layout(geo=dict(showframe=False,showcoastlines=False,projection_type='equirectangular'))
        st.plotly_chart(fig)
    
    col7,col8=st.columns(2)
    
    
    with col7:
        value_count=df['product_type'].value_counts()
        fig15=px.bar(x=value_count.index[0:10], y=value_count.values[0:10], color=value_count.values[0:10],color_discrete_sequence='agsunset',title='Top 10 Products',labels={'x':'Product','y':'Count'})
        fig15.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig15)
    
    
    with col8:
        product_type_to_analyze=value_count.index[0:10]
        
        filtered_df = df[df['product_type'].isin(product_type_to_analyze)]
        
        average_prices = filtered_df.groupby('product_type')[['price_usd', 'seller_price', 'seller_earning', 'buyers_fees']].mean()
    
        fig17 = px.bar(average_prices,title='Average Prices based on Product Type', labels={'x': 'Brand', 'y': 'Average Price','variable':'Price Type'})
        
        fig17.update_layout(xaxis_tickangle=-45, legend_title_text='Price Type')
        st.plotly_chart(fig17)
    
    
    col9,col10,col11=st.columns(3)
    
    
    with col9:
        
        value_count = df['usually_ships_within'].value_counts().reset_index()
        value_count.columns = ['shipping_time', 'Count']
    
        
        fig20 = px.bar(value_count, 
                    x='shipping_time', 
                    y='Count', 
                    title='Distribution of Shipping Times',
                    labels={'shipping_time': 'Shipping Time', 'Count': 'Count'},
                    color='shipping_time',
                    color_continuous_scale='Viridis')
    
        
        fig20.update_layout(xaxis_tickangle=-90,width=350)
        st.plotly_chart(fig20)
    
    
    with col10:
    
        category_feature1 = 'usually_ships_within'  
        category_feature2 = 'product_category'  
        fig21 = px.histogram(df, 
                        x=category_feature2, 
                        color=category_feature1, 
                        barmode='group',
                        title='Count of Shipping Times by Product Category',
                        labels={category_feature2: 'Product Category', 'count': 'Count', category_feature1: 'Shipping Time'},
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    
        
        fig21.update_layout(xaxis_tickangle=-45, 
                        yaxis_title='Count', 
                        xaxis_title='Product Category',width=350)
        st.plotly_chart(fig21)
    
    
    with col11:
        
        category_feature1 = 'usually_ships_within'  
        category_feature2 = 'warehouse_name'  
    
        
        fig22 = px.histogram(df, 
                        x=category_feature2, 
                        color=category_feature1, 
                        barmode='group',
                        title='Count of Shipping Times by Warehouse Name',
                        labels={category_feature2: 'Warehouse Name', 'count': 'Count', category_feature1: 'Shipping Time'})
    
        
        fig22.update_layout(xaxis_tickangle=-45, 
                        yaxis_title='Count', 
                        xaxis_title='Warehouse Name',width=350)
        st.plotly_chart(fig22)
    
    
    col12,col13=st.columns(2)
    
    
    with col12:
        
        country_counts = df['seller_country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']
    
        
        fig24 = px.choropleth(country_counts, 
                            locations='Country', 
                            locationmode='country names', 
                            color='Count',
                            color_continuous_scale='viridis',
                            title='Seller Distribution by Country')
    
        
        fig24.update_layout(geo=dict(showframe=False, 
                                    projection_type='equirectangular'),
                        coloraxis_colorbar=dict(title='Count'))
        st.plotly_chart(fig24)
    
    
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    
    with col13:
        
        warehouse = df.groupby('seller_country')['warehouse_name'].value_connts().reset_index()
    
        
        fig = px.choropleth(
            warehouse,
            locations='seller_country',
            locationmode='country names',
            color='warehouse_name',
            title='Most Common warehouse by Country',
            color_continuous_scale=px.colors.sequential.Plasma,
        )
        fig.update_layout()
        st.plotly_chart(fig)



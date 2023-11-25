import pymysql
import pandas as pd 
import os
import json
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

#sql_connection 
myconnection=pymysql.connect(host="127.0.0.1",
                             user="root",
                             password="kishore22",
                             database="Phonepe")

cursor=myconnection.cursor()

#Aggregated_transaction
Aggregated_transaction=pd.read_sql_query("select * from Aggregated_transaction",myconnection)

#Aggregated_user
Aggregated_user=pd.read_sql_query("select * from Aggregated_user",myconnection)

#Map_transaction
Map_transaction=pd.read_sql_query("select * from Map_transaction",myconnection)

#Map_user
Map_user=pd.read_sql_query("select * from Map_user",myconnection)

#Top_transaction
Top_transaction=pd.read_sql_query("select * from Top_transaction",myconnection)

#Top_user
Top_user=pd.read_sql_query("select * from Top_user",myconnection)



#Page_configuration
st.set_page_config(page_title="Phonepe Pulse data Visualization | by Kishore Kumar",
                   layout="wide")



st.sidebar.header(":violet[Welcome to the Dashboard]")


#Option menu in sidebar
with st.sidebar:
    selected = option_menu("Menu",["Home","Top_Chart","Explore_Data"],
                icons=["house","graph-up-arrow",'bar-chart-line'],
                orientation='vertical')


#Menu1-Home
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")

    st.write(" ")
    
    st.markdown(":violet[A User-Friendly Tool Using Streamlit and Plotly]")
    
    st.write(" ")

    st.write(" ")

    st.markdown(":green[Overview :]With the help of this streamlit web application, you can see the phonepe pulse data and learn a lot about transactions, user count, pincodes, top 10 states, districts, and brands with the most users, among other things. To obtain some insights, visualisations such as pie charts, bar charts, and geomapping are used.")
    
    st.write(" ")
    
    st.markdown(":green[Technology Used :]Github Cloning,Python,Pandas,MySql,Stremlit and plotly.")
    
    st.write(" ")
    
    st.markdown(""":green[Required Libraries :]
                                                pymysql,
                                                pandas,
                                                os,
                                                json,
                                                streamlit,
                                                plotly.express,
                                                plotly.graph_objects,
                                                streamlit_option_menu""")
    

#Menu2-Top_Chart
if selected=="Top_Chart":
    st.markdown("# :red[Top_Chart]")
    Type=st.sidebar.selectbox("**Type**",("Transactions","Users"))

    Year=st.sidebar.slider("**Year**",min_value=2018,max_value=2022)
    Quaters=st.sidebar.slider("**Quaters**",min_value=1,max_value=4)

    st.info(
            """
            #### From this menu we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """,icon="🔍"
            )
 
    if Type == "Transactions":
        col1,col2,col3=st.columns([1,1,1],gap="small")

        with col1:
            st.markdown("# :violet[State]")
            cursor.execute(f"select State,sum(Transaction_count) as Total_Transation_count,sum(Transaction_amount) as Total_Amount from Aggregated_transaction where Year= {Year} and Quaters = {Quaters} group by State order by Total_Amount desc limit 10")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig=px.pie(df,values="Total_Amount",
                        names="State",
                        title="Top 10",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=["Transactions_Count"],
                        labels={"Transaction_Count":"Transaction_Count"})
            
            fig.update_traces(textposition="inside",textinfo="percent+label")
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("# :red[District]")
            cursor.execute(f"select District,sum(Transaction_count) as Total_Transaction_count,sum(Transaction_amount) as Total_amount from Map_transaction where Year = {Year} and Quaters = {Quaters} group by District order by Total_amount desc limit 10;")
            df=pd.DataFrame(cursor.fetchall(),columns=["District","Transactions_Count","Total_Amount"])
            fig=px.pie(df,values="Total_Amount",
                        names="District",
                        title="Top 10",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=["Transactions_Count"],
                        labels={"Transaction_Count":"Transaction_Count"})
            
            fig.update_traces(textposition="inside",textinfo="percent+label")
            st.plotly_chart(fig,use_container_width=True)

        with col3:
            st.markdown("# :blue[Pincode]")
            cursor.execute(f"select Pincodes,sum(Transaction_count) as Total_Transaction_count,sum(Transaction_amount) as Total_amount from Top_transaction where Year = {Year} and Quaters = {Quaters} group by Pincodes order by Total_amount desc limit 10;")
            df=pd.DataFrame(cursor.fetchall(),columns=["Pincodes","Transactions_Count","Total_Amount"])
            fig=px.pie(df,values="Total_Amount",
                        names="Pincodes",
                        title="Top 10",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=["Transactions_Count"],
                        labels={"Transaction_Count":"Transaction_Count"})
            
            fig.update_traces(textposition="inside",textinfo="percent+label")
            st.plotly_chart(fig,use_container_width=True)

    if Type == "Users":
        col1,col2=st.columns([2,2],gap="small")

        with col1:
            st.markdown("# :violet[Brand]")
            if Year == 2022 and Quaters in[2,3,4]:
                st.markdown("#### Sorry No Data to display for 2022 Quaters 2,3,4")
            else:
                cursor.execute(f"select Brand,sum(Transaction_count) as Total_count,avg(Percentage) as Avg_percentage from Aggregated_user where Year={Year} and Quaters = {Quaters} group by Brand order by Total_count desc limit 10;")
                df=pd.DataFrame(cursor.fetchall(),columns=["Brand","Total_users","Avg_percentage"])
                fig=px.bar(df,title="Top 10",
                            x="Total_users",
                            y="Brand",
                            orientation="h",
                            color="Avg_percentage",
                            color_discrete_sequence=px.colors.sequential.Agsunset)

                st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("# :red[District]")
            cursor.execute(f"select District,sum(Regsistered_User) as Total_users,sum(App_Opens) as Total_AppOpens from Map_user where Year ={Year} and Quaters ={Quaters} group by District order by Total_users desc limit 10;")
            df=pd.DataFrame(cursor.fetchall(),columns=["District","Total_users","Total_AppOpens"])
            fig=px.bar(df,title="Top 10",
                       x="Total_users",
                       y="District",
                       orientation="h",
                       color="Total_AppOpens",
                       color_continuous_midpoint=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

        col3,col4=st.columns([2,2],gap="small")
        with col3:
            st.markdown("# :green[Pincode]")
            cursor.execute(f"select Pincodes,sum(RegisteredUser) as Total_users from Top_user where Year = {Year} and Quaters = {Quaters} group by Pincodes order by Total_users desc limit 10;")
            df=pd.DataFrame(cursor.fetchall(),columns=["Pincodes","Total_users"])
            fig=px.pie(df,values="Total_users",
                        names="Pincodes",
                        title="Top 10",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=["Total_users"])
            
            fig.update_traces(textposition="inside",textinfo="percent+label")
            st.plotly_chart(fig,use_container_width=True)

        with col4:
            st.markdown("# :blue[State]")
            cursor.execute(f"select State,sum(Regsistered_User) as Total_users,sum(App_Opens) as Total_AppOpens from Map_user where Year = {Year} and Quaters = {Quaters} group by State order by Total_users desc limit 10 ;")
            df=pd.DataFrame(cursor.fetchall(),columns=["State","Total_users","Total_AppOpens"])
            fig=px.pie(df,values="Total_users",
                        names="State",
                        title="Top 10",
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=["Total_AppOpens"])
            
            fig.update_traces(textposition="inside",textinfo="percent+label")
            st.plotly_chart(fig,use_container_width=True)


#Menu3-Explore Data
if selected == "Explore_Data":
    Type=st.sidebar.selectbox("**Type**",("Transactions","Users"))
    Year=st.sidebar.slider("**Year**",min_value=2018,max_value=2022)
    Quaters=st.sidebar.slider("**Quaters**",min_value=1,max_value=4)

    col1,col2=st.columns(2)

    if Type == "Transactions":

        with col1:
            st.markdown("### :green[Overall State Data - Transaction Amount]")
            cursor.execute(f"select State, sum(Transaction_count) as Total_transaction, sum(Transaction_amount) as Total_amount from Map_Transaction where Year= {Year} and Quaters = {Quaters} group by State order by State;")
            df=pd.DataFrame(cursor.fetchall(),columns=["States","Total_transactions","Total_amount"])

            fig=px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey="properties.ST_NM",
                              locations="States",
                              color="Total_amount",
                              color_continuous_scale="sunset")
            
            fig.update_geos(fitbounds="locations",visible=False)
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            st.markdown("### :blue[Overall State Data - Transaction Count]")
            cursor.execute(f"select State, sum(Transaction_count) as Total_transaction, sum(Transaction_amount) as Total_amount from Map_Transaction where Year= {Year} and Quaters = {Quaters} group by State order by State;")
            df=pd.DataFrame(cursor.fetchall(),columns=["States","Total_transactions","Total_amount"])

            fig=px.choropleth(df,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                              featureidkey="properties.ST_NM",
                              locations="States",
                              color="Total_transactions",
                              color_continuous_scale="sunset")
            
            fig.update_geos(fitbounds="locations",visible=False)
            st.plotly_chart(fig,use_container_width=True)

#Bar_Chart - Top Payment Type 
        st.markdown("## :red[Top Payment Type]")
        cursor.execute(f"select Transaction_type,sum(Transaction_count) as Total_count, sum(Transaction_amount) as Total_amount from Aggregated_transaction where Year={Year} and Quaters={Quaters} group by Transaction_type order by Transaction_type;")  
        df=pd.DataFrame(cursor.fetchall(),columns=["Transaction_type","Total_count","Total_amount"])

        fig=px.bar(df,title="Transaction Type vs Total transactions",
                   x="Transaction_type",
                   y="Total_count",
                   orientation="v",
                   color="Total_amount",
                   color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)

# BAR CHART TRANSACTIONS - DISTRICT WISE DATA 
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown("## :green[Select any State to Explore More]")
        selected_state=st.selectbox("",
                                    ("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar",
                                    "Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi",
                                    "Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand",
                                    "Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra",
                                    "Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                    "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
                                    "Uttar Pradesh","Uttarakhand","West Bengal"),index=30)
        
        cursor.execute(f"select State,Year,Quaters,District,sum(Transaction_count) as Total_transaction,sum(Transaction_amount) as Total_amount from Map_transaction where Year={Year} and Quaters = {Quaters} and State = '{selected_state}' group by State,Year,Quaters,District order by State,District;")
        df=pd.DataFrame(cursor.fetchall(),columns=["State","Year","Quaters","District","Total_transaction","Total_amount"])

        fig=px.bar(df,title=selected_state,
                   x="District",
                   y="Total_transaction",
                   orientation="v",
                   color="Total_amount",
                   color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

#Explore Data -Users

    if Type == "Users":
        st.markdown("## :green[Select any State to Explore More]")
        selected_state=st.selectbox("",
                                    ("Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar",
                                    "Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi",
                                    "Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir","Jharkhand",
                                    "Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra",
                                    "Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab",
                                    "Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
                                    "Uttar Pradesh","Uttarakhand","West Bengal"),index=30)
        
        cursor.execute(f"select State,Year,Quaters,District,sum(Regsistered_User) as Total_users,sum(App_Opens) as Total_AppOpens from map_user where Year={Year} and Quaters = {Quaters} and State = '{selected_state}' group by State,Year,Quaters,District order by State,District;")
        df=pd.DataFrame(cursor.fetchall(),columns=["State","Year","Quaters","District","Total_users","Total_AppOpens"])

        fig=px.bar(df,title=selected_state,
                   x="District",
                   y="Total_users",
                   orientation="v",
                   color="Total_AppOpens",
                   color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)
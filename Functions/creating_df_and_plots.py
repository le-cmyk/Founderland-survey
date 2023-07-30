import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st




def calculate_column_percentages(df, columns_of_interest):
    # Calculate the total number of respondents
    total_respondents = len(df)
    
    # Create a DataFrame to store the percentages
    df_percentages = pd.DataFrame(columns=['Attribute', 'Percentage'])
    
    # Calculate the percentage for each attribute in the specified columns
    for column in columns_of_interest:
        percentages_valeur  = df[column].count()/total_respondents*100
        percentages_df = pd.DataFrame({'Attribute': [column], 'Percentage': [round(percentages_valeur,2)]})
        df_percentages = df_percentages.append(percentages_df, ignore_index=True)

    
    return df_percentages.sort_values(by="Percentage",ascending= False)

def create_stacked_barplot(df, x, y, titre):
    # Calcul de la marge de progression vers 100
    df['Progress'] = 100 - df[y]
    
    # Création du barplot avec Plotly
    fig = go.Figure()
    
    # Barplot unique avec le pourcentage et la marge de progression empilés
    fig.add_trace(go.Bar(
        x=df[x],
        y=df[y],
        name='Percentage',
        text=df[y].apply(lambda x: f"{x:.2f}%"),
        textposition='auto',
        marker=dict(color='blue', line=dict(color='blue', width=1)),  # Style pour le pourcentage
        opacity=0.8  # Opacité pour donner un style plus moderne
    ))
    
    fig.add_trace(go.Bar(
        x=df[x],
        y=df['Progress'],
        name='Progress to 100',
        text=df['Progress'].apply(lambda x: f"{x:.2f}%"),
        textposition='inside',  # Pour afficher le pourcentage au centre de la partie rouge
        marker=dict(color='red', line=dict(color='red', width=1)),  # Style pour la marge de progression
        opacity=0.8  # Opacité pour donner un style plus moderne
    ))
    
    # Mise en forme du graphe
    fig.update_layout(
        title=titre,
        xaxis_title='Attribut',
        yaxis_title='Pourcentage',
        barmode='relative',  # Utilise le mode relatif pour empiler les deux valeurs
    )
    
    return fig


def calculate_event_occurrences(df, column_name):
    # Créer une liste de dictionnaires pour chaque ligne de la colonne
    dict_list = df[column_name].str.replace("\\, ", "").str.split(",").apply(lambda row_values: {event: index for index, event in enumerate(row_values)})
    
    # Initialiser un dictionnaire pour stocker la somme par événement
    event_occurrences = {}

    # Parcourir chaque dictionnaire et faire la somme
    for d in dict_list:
        for event, occurrence in d.items():
            event_occurrences[event] = event_occurrences.get(event, 0) + occurrence

    # Convertir le dictionnaire en un DataFrame
    df_occurrences = pd.DataFrame(list(event_occurrences.items()), columns=['Event', 'Occurrences']).sort_values(by="Occurrences", ascending=True).reset_index(drop=True).reset_index(drop=False)[['index', 'Event']]

    # Renommer les colonnes de façon plus descriptive
    df_occurrences = df_occurrences.rename(columns={'index': 'Frequency Rank', 'Event': 'Event Name', 'Occurrences': 'Event Occurrences'})
    df_occurrences['Frequency Rank'] = df_occurrences['Frequency Rank']+1

    return df_occurrences


def create_horizontal_bar_chart(df, title):
    # Sort the DataFrame by 'Frequency Rank' in descending order
    df_sorted = df.sort_values(by='Frequency Rank', ascending=False)

    # Define a color scale from green to red
    color_scale = [(0, 'green'), (1, 'red')]

    # Create the horizontal bar chart using Plotly
    fig = go.Figure()

    # Barplot with custom colors and text position
    fig.add_trace(go.Bar(
        x=df_sorted['Frequency Rank'],
        y=df_sorted['Event Name'],
        orientation='h',  # Horizontal orientation for the bar chart
        marker=dict(color=df_sorted['Frequency Rank'], coloraxis="coloraxis"),  # Use the color scale for the bars
        opacity=0.8,
        text=df_sorted['Frequency Rank'],  # Display the Frequency Rank as text on top of the bars
        textposition='inside',  # Display the text inside the bars
        insidetextanchor='start',  # Anchor the text at the start of the bars (top for horizontal bars)
    ))

    # Mise en forme du graphe
    fig.update_layout(
        title=title,
        xaxis_title='Preference',
        yaxis_title='Name',
        coloraxis=dict(colorscale=color_scale,showscale=False),
        showlegend=True,  # Hide the legend to remove the colorbar
    )

    return fig

def plot_box_with_mean(df, x, y, title="", legend_mapping=None):
    # Calcul de la moyenne pour chaque classe
    mean_df = df.groupby(y)[x].mean().sort_values(ascending=True).reset_index()
    mean_df.rename(columns={x: f"mean_{x}"}, inplace=True)

    med_df = df.groupby(y)[x].median().reset_index()
    med_df.rename(columns={x: f"med_{x}"}, inplace=True)

    # Create the horizontal bar chart using Plotly
    fig = go.Figure()

    # Define a color scale from green to red
    color_scale = [(0, 'red'), (1, 'green')]

    # Barplot with custom colors and text position
    fig.add_trace(go.Bar(
        x=mean_df['mean_Value'],
        y=mean_df['Column Name'],
        orientation='h',  # Horizontal orientation for the bar chart
        marker=dict(color=mean_df['mean_Value'], coloraxis="coloraxis"),  # Use the color scale for the bars,
        name="mean",
        showlegend=True
        ))


    # Create a single trace for the median circle
    median_trace_x = med_df[f"med_{x}"]
    median_trace_y = med_df[y]
    fig.add_trace(
        go.Scatter(
            x=median_trace_x,
            y=median_trace_y,
            mode="markers",
            marker=dict(color="yellow", size=10, symbol='circle'),  # Utiliser un cercle
            name="Median",  # Add a name for the median trace
            showlegend=True  # Show the legend for the median trace
        )
    )

    # Définir les étiquettes de légende personnalisées
    if legend_mapping:
        ticktext = [label for label in legend_mapping.keys()]
        tickvals = [value for value in legend_mapping.values()]
        fig.update_xaxes(ticktext=ticktext, tickvals=tickvals)

    # Mise en forme du graphique
    fig.update_layout(
        title=title,
        xaxis=dict(type='linear'),  # Définir l'échelle de l'axe x en linéaire
        legend_title_text="Legend",
        legend_traceorder="reversed",
        coloraxis=dict(colorscale=color_scale,showscale=False)
    )

    return fig


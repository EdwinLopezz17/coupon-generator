import pandas as pd

def validate_sku_coupons(cupones_sku_file, productos_df):
    cupones_sku_df = pd.read_excel(cupones_sku_file)
    cupones_sku_df.columns = cupones_sku_df.columns.str.strip()

    cupones_sku_df['Producto válido'] = cupones_sku_df['Código Producto'].isin(productos_df['Code'])
    cupones_sku_df['Fechas correctas'] = pd.to_datetime(
        cupones_sku_df['Vigencia Desde'], errors='coerce'
    ) < pd.to_datetime(
        cupones_sku_df['Vigencia Hasta'], errors='coerce'
    )

    cupones_sku_df['Descuento válido'] = cupones_sku_df.apply(_validate_discount, axis=1)

    cupones_sku_df['Error'] = ""
    cupones_sku_df.loc[~cupones_sku_df['Producto válido'], 'Error'] += "Código inválido. "
    cupones_sku_df.loc[~cupones_sku_df['Fechas correctas'], 'Error'] += "Fechas inválidas. "
    cupones_sku_df.loc[~cupones_sku_df['Descuento válido'], 'Error'] += "Descuento inválido. "

    errores_df = cupones_sku_df[cupones_sku_df['Error'] != ""]
    return cupones_sku_df, errores_df

def validate_category_coupons(cupones_categoria_file, productos_df):
    cupones_cat_df = pd.read_excel(cupones_categoria_file)
    cupones_cat_df.columns = cupones_cat_df.columns.str.strip()

    categorias_unicas = productos_df['Categoría'].unique()
    cupones_cat_df['Categoría válida'] = cupones_cat_df['Categoría'].isin(categorias_unicas)
    cupones_cat_df['Fechas correctas'] = pd.to_datetime(
        cupones_cat_df['Vigencia Desde'], errors='coerce'
    ) < pd.to_datetime(
        cupones_cat_df['Vigencia Hasta'], errors='coerce'
    )

    cupones_cat_df['Descuento válido'] = cupones_cat_df.apply(_validate_discount, axis=1)

    cupones_cat_df['Error'] = ""
    cupones_cat_df.loc[~cupones_cat_df['Categoría válida'], 'Error'] += "Categoría inválida. "
    cupones_cat_df.loc[~cupones_cat_df['Fechas correctas'], 'Error'] += "Fechas inválidas. "
    cupones_cat_df.loc[~cupones_cat_df['Descuento válido'], 'Error'] += "Descuento inválido. "

    errores_df = cupones_cat_df[cupones_cat_df['Error'] != ""]
    return cupones_cat_df, errores_df

def expand_category_coupons(cupones_cat_df, productos_df):
    if cupones_cat_df.empty:
        return pd.DataFrame()

    expanded = []
    for _, row in cupones_cat_df.iterrows():
        products = productos_df[productos_df['Categoría'] == row['Categoría']]
        for _, prod in products.iterrows():
            expanded.append({
                'Código Producto': prod['Code'],
                'Tipo Descuento': row['Tipo Descuento'],
                'Valor': row['Valor'],
                'Vigencia Desde': row['Vigencia Desde'],
                'Vigencia Hasta': row['Vigencia Hasta'],
                'Marca': prod['Marca'],
                'Categoría': prod['Categoría'],
                'Productos': prod['Productos'],
                'Agrupación': prod['Agrupación']
            })
    return pd.DataFrame(expanded)

def merge_sku_with_products(cupones_sku_df, productos_df):
    if cupones_sku_df.empty:
        return pd.DataFrame()

    merged = cupones_sku_df.merge(
        productos_df,
        left_on='Código Producto',
        right_on='Code',
        how='left'
    )
    return merged[[
        'Código Producto',
        'Tipo Descuento',
        'Valor',
        'Vigencia Desde',
        'Vigencia Hasta',
        'Marca',
        'Categoría',
        'Productos',
        'Agrupación'
    ]]

def _validate_discount(row):
    if row['Tipo Descuento'].lower() == 'porcentaje':
        return (0 < row['Valor'] <= 100)
    elif row['Tipo Descuento'].lower() == 'monto':
        return row['Valor'] > 0
    else:
        return False

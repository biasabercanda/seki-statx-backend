# SEKI STATX BACKEND

## Flask RESTful + Vercel

This API is built using Flask RESTful and deployed on Vercel.

## How to Use

Call the API and pass the table ID. You can see the table ID in [SEKI Page](https://www.bi.go.id/id/statistik/ekonomi-keuangan/seki/Default.aspx), on the PDF donwload button.

`https://seki-statx-api.vercel.app/<table_id>`

example: `https://seki-statx-api.vercel.app/TABEL1_1`

## How it Works

This API request an excel file from the [SEKI Page](https://www.bi.go.id/id/statistik/ekonomi-keuangan/seki/Default.aspx) provided by Bank Indonesia and transforms it using Pandas library. It sends the JSON data as a response. **Currently this API only extract data from 2010-newest**.

:root
{
    --bg : #f7f9fb;
    --card : #ffffff;
    --muted : #6b7280;
    --accent : #0b69ff;
    --accent - 2 : #06b6d4;
    --radius : 12px;
    --shadow : 0 6px 18px rgba(20, 30, 50, 0.06);
}

*
{
    box - sizing : border - box;
    font - family : Inter, ui - sans - serif, system - ui, -apple - system, Segoe UI, Roboto, "Helvetica Neue", Arial
}
body
{
margin:
    0;
background:
    var(--bg);
color:
# 111;
    -webkit - font - smoothing : antialiased;
}

.topbar
{
display:
    flex;
    align - items : center;
    justify - content : space - between;
padding:
    18px 28px;
background:
    white;
    border - bottom : 1px solid rgba(16, 24, 40, 0.04);
}
.brand
{
display:
    flex;
gap:
    12px;
    align - items : center
}
.logo
{
width:
    48px;
height:
    48px;
    border - radius : 8px;
    object - fit : cover;
border:
    1px solid rgba(16, 24, 40, 0.04)
}
.title - area h1
{
margin:
    0;
    font - size : 18px;
    letter - spacing : 0.2px
}
.subtitle
{
margin:
    0;
    font - size : 12px;
color:
    var(--muted)
}

.container
{
padding:
    24px 28px;
    max - width : 1100px;
margin:
    18px auto
}
.grid
{
display:
    grid;
    grid - template - columns : 1fr 420px;
gap:
    18px
}
@media(max - width : 900px){.grid{grid - template - columns : 1fr;
}
}
.card
{
background:
    var(--card);
    border - radius : var(--radius);
padding:
    16px;
    box - shadow : var(--shadow);
border:
    1px solid rgba(16, 24, 40, 0.03)
}
.price - card.card - head
{
display:
    flex;
    justify - content : space - between;
    align - items : center
}
.price
{
    font - weight : 700;
    font - size : 28px
}
.price - box
{
display:
    flex;
    flex - direction : column;
    align - items : flex - end
}
.muted{color : var(--muted)}
        .small{font - size : 12px}
        .card -
    body{margin - top : 8px}
        .price -
    body{margin - top : 10px}
        .card -
    foot
{
    margin - top : 12px;
    border - top : 1px dashed rgba(0, 0, 0, 0.04);
    padding - top : 10px
}

.order - card h3{margin - top : 0}.order - form label
{
display:
    block;
    margin - bottom : 8px;
    font - size : 13px
}
.order - form input, .order - form select
{
width:
    100 % ;
padding:
    8px;
    border - radius : 8px;
border:
    1px solid rgba(16, 24, 40, 0.08);
outline:
    none;
    font - size : 14px;
background:
    transparent
}
.row
{
display:
    flex;
gap:
    12px;
    margin - bottom : 12px
}
.row label{flex : 1}
    .actions
{
display:
    flex;
gap:
    10px;
    align - items : center
}
.btn
{
border:
    0;
padding:
    8px 12px;
    border - radius : 8px;
cursor:
    pointer;
background:
    white;
border:
    1px solid rgba(16, 24, 40, 0.06)
}
.btn.primary
{
background:
    var(--accent);
color:
    white;
border:
    none;
    box - shadow : 0 6px 18px rgba(11, 105, 255, 0.12)
}
.btn.outline
{
background:
    transparent;
border:
    1px solid rgba(16, 24, 40, 0.08)
}
.btn.small
{
padding:
    6px 8px;
    font - size : 13px;
    border - radius : 8px
}
.result
{
background:
#fbfdff;
border:
    1px solid rgba(11, 105, 255, 0.06);
padding:
    10px;
    border - radius : 8px;
    margin - top : 12px
}

.quick - card.quick - grid
{
display:
    flex;
    flex - direction : column;
gap:
    8px
}
.quick - grid button
{
width:
    100 % ;
    text - align : left
}

.footer
{
padding:
    18px;
    text - align : center;
color:
    var(--muted);
background:
    transparent;
    border - top : 1px solid rgba(16, 24, 40, 0.03);
    margin - top : 12px
}

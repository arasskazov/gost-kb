<table>
<colgroup>
<col style="width: 27%" />
<col style="width: 2%" />
<col style="width: 41%" />
<col style="width: 2%" />
<col style="width: 25%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="5"><p><strong>Федеральное агентство</strong></p>
<p><strong>по техническому регулированию и метрологии</strong></p></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><img src="standards/77-304/media/media/image1.png" style="width:1.42708in;height:0.89583in" /></td>
<td></td>
<td><p><strong>НАЦИОНАЛЬНЫЙ</strong></p>
<p><strong>СТАНДАРТ</strong></p>
<p><strong>РОССИЙСКОЙ</strong></p>
<p><strong>ФЕДЕРАЦИИ</strong></p></td>
<td></td>
<td><p><strong>ГОСТ Р</strong></p>
<p><strong>77.304―</strong></p>
<p><strong>202Х</strong></p>
<p><em>(проект, первая<br />
редакция)</em></p></td>
</tr>
</tbody>
</table>

**Система поддержки жизненного цикла изделия**

**ИНФОРМАЦИОННАЯ МОДЕЛЬ ИЗДЕЛИЯ**

**Представление свойств**

*Настоящий проект стандарта не подлежит применению до его утверждения*

**Предисловие**

1 РАЗРАБОТАН Акционерным обществом «Научно-исследовательский центр «Прикладная Логистика» (АО «НИЦ «Прикладная Логистика»), Обществом с ограниченной ответственностью «АСКОН-Бизнес-Решения» (ООО «АСКОН-Бизнес-Решения»), Закрытым акционерным обществом «Топ Системы» (ЗАО «Топ Системы»)

2 ВНЕСЕН Техническим комитетом по стандартизации ТК 482 «Поддержка жизненного цикла продукции»

3 УТВЕРЖДЕН И ВВЕДЕН В ДЕЙСТВИЕ Приказом Федерального агентства по техническому регулированию и метрологии от

4 ВВЕДЕН ВПЕРВЫЕ

*Правила применения настоящего стандарта установлены в статье 26 Федерального закона от 29 июня 2015 г. № 162-ФЗ «О стандартизации в Российской Федерации». Информация об изменениях к настоящему стандарту публикуется в ежегодном (по состоянию на 1 января текущего года) информационном указателе «Национальные стандарты», а официальный текст изменений и поправок – в ежемесячном информационном указателе «Национальные стандарты». В случае пересмотра (замены) или отмены настоящего стандарта соответствующее уведомление будет опубликовано в ближайшем выпуске ежемесячного информационного указателя «Национальные стандарты». Соответствующая информация, уведомление и тексты размещаются также в информационной системе общего пользования – на официальном сайте Федерального агентства по техническому регулированию и метрологии в сети Интернет (www.rst.gov.ru)*

© Оформление. ФГБУ «Институт стандартизации», 202

Настоящий стандарт не может быть полностью или частично воспроизведен, тиражирован и распространен в качестве официального издания без разрешения Федерального агентства по техническому регулированию и метрологии**  
**

**Содержание**

[1 Область применения](#_Toc445998457)

[2 Нормативные ссылки](#_Toc467869760)

[3 Термины, определения и сокращения](#_Toc467869761)

[4 Общие положения](#_Toc224213438)

[5 Идентификация свойств](#_Toc224213439)

[6 Значения свойств](#_Toc224213440)

[7 Представления](#_Toc224213441)

> [7.1 Общие сведения о представлениях](#общие-сведения-о-представлениях)
>
> [7.2 Связи между представлениями и элементами представления](#связи-между-представлениями-и-элементами-представления)
>
> [7.3 Преобразование элементов представления](#преобразование-элементов-представления)
>
> [7.4 Неточность представления](#погрешность-представления)

[Приложение А (справочное) Формализованное описание информационной модели на языке Express](#_Toc224213446)

**НАЦИОНАЛЬНЫЙ СТАНДАРТ российской федерации**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Система поддержки жизненного цикла изделия</strong></p>
<p><strong>ИНФОРМАЦИОННАЯ МОДЕЛЬ ИЗДЕЛИЯ</strong></p>
<p><strong>Представление свойств</strong></p>
<p>Product life cycle support system. Product information model.</p>
<p>Property representation</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Дата введения ―**

1.  <span id="_Toc445998457" class="anchor"></span>Область применения

Настоящий стандарт определяет составную часть интегрированной схемы данных, используемой для создания и применения информационной модели изделия машиностроения.

Стандарт устанавливает схему данных для представления свойств объектов разной природы.

2.  <span id="_Toc467869760" class="anchor"></span>Нормативные ссылки

В настоящем стандарте использованы нормативные ссылки на следующие стандарты:

ГОСТ Р 2.005  Единая система конструкторской документации. Термины и определения

ГОСТ Р 77.002  Система поддержки жизненного цикла изделия. Термины и определения *(проект, окончательная редакция, разрабатывается совместно)*

ГОСТ Р 77.301  Система поддержки жизненного цикла изделия. Информационная модель изделия. Основные положения *(проект, первая редакция, разрабатывается совместно)*

ГОСТ Р ИСО 10303–11 Системы автоматизации производства и их интеграция. Представление данных об изделии и обмен этими данными. Часть 11. Методы описания. Справочное руководство по языку EXPRESS

ГОСТ Р ИСО 10303–41 Системы автоматизации производства и их интеграция. Представление данных об изделии и обмен этими данными. Часть 41. Интегрированный обобщенный ресурс. Основы описания и поддержки изделий

ГОСТ Р ИСО 10303–43 Системы автоматизации производства и их интеграция. Представление данных об изделии и обмен этими данными. Часть 43. Интегрированный обобщенный ресурс. Структуры представления

Примечание  При пользовании настоящим стандартом целесообразно проверить действие ссылочных стандартов в информационной системе общего пользования – на официальном сайте Федерального агентства по техническому регулированию и метрологии в сети Интернет или по ежегодному информационному указателю «Национальные стандарты», который опубликован по состоянию на 1 января текущего года, и по выпускам ежемесячного информационного указателя «Национальные стандарты» за текущий год. Если заменен ссылочный стандарт, на который дана недатированная ссылка, то рекомендуется использовать действующую версию этого стандарта с учетом всех внесенных в данную версию изменений. Если заменен ссылочный стандарт, на который дана датированная ссылка, то рекомендуется использовать версию этого стандарта с указанным выше годом утверждения (принятия). Если после утверждения настоящего стандарта в ссылочный стандарт, на который дана датированная ссылка, внесено изменение, затрагивающее положение, на которое дана ссылка, то это положение рекомендуется применять без учета данного изменения. Если ссылочный стандарт отменен без замены, то положение, в котором дана ссылка на него, рекомендуется применять в части, не затрагивающей эту ссылку.

3.  <span id="_Toc467869761" class="anchor"></span>Термины, определения и сокращения

3.1 В настоящем стандарте применены термины по ГОСТ Р 2.005 и ГОСТ Р 77.002, а также следующие термины и определения:

3.1.1 **схема данных:** Формальное описание организации данных, в том числе описание элементов данных, взаимосвязей между ними, типов данных, возможных значений и ограничений.

3.1.2

**свойство продукции:** Объективная особенность продукции, которая может проявляться при ее создании, эксплуатации или потреблении.

\[ГОСТ 15467-79\]

Примечание – Простые свойства выражаются конкретным значением (числовым, булевым, текстовым и т. п.), а сложные (например, «надёжность», «форма») выражаются более сложными информационными конструкциями: группой значений, таблицей значений, совокупностью геометрических примитивов и т. п.).

3.1.3 **представление** (representation): Набор связанных элементов данных, используемый для представления информации о свойстве объекта в контексте решения конкретной задачи.

3.1.4 **контекст представления** (context of representation): это именованная (идентифицированная) точка зрения или задача, для которой используется представление.

3.1.5 **элемент представления** (representation item): Элемент данных, входящий в состав представления непосредственно, либо через другие элементы.

3.2 В настоящем стандарте применены следующие сокращения:

| ЕСКД |     | Единая система конструкторской документации; |                                                                 |     |
|------|-----|----------------------------------------------|-----------------------------------------------------------------|-----|
| ИО   |     | информационный объект;                       |                                                                 |     |
| СЧ   |     | составная часть;                             |                                                                 |     |
| UML  |    |                                              | unified modeling language (унифицированный язык моделирования). |     |

4.  <span id="_Toc224213438" class="anchor"></span>Общие положения

    1.  Установленные настоящим стандартом схемы данных базируются не схемах:

        \- product_property_definition (ГОСТ Р ИСО 10303-41);

        \- product_property_representation (ГОСТ Р ИСО 10303-41);

        \- representation (ГОСТ Р ИСО 10303-43).

    2.  Приведенные в настоящем стандарте схемы данных адаптированы и дополнены с учетом терминологии и требований стандартов ЕСКД и могут быть использованы для представления свойств изделий машиностроения, разрабатываемых в соответствии со стандартами ЕСКД, и их СЧ (в т. ч. материалов, программных продуктов, документов)

    3.  Схемы данных позволяют описывать:

\- номенклатуры свойств, которыми может обладать изделие, материал, программное изделие, документ;

\- конкретные значения свойств (численных, текстовых и т. п.), присущих конкретным экземплярам объектов (изделию, материалу, программному изделию, документу);

\- наборы элементов данных, составляющих значение сложного свойства (например, форма объекта, определенная как совокупность геометрических и топологических элементов) – представлений.

5.  <span id="_Toc224213439" class="anchor"></span>Идентификация свойств

    1.  Правила идентификации свойств основаны на схеме данных product_property_definition_schema, установленной в ГОСТ Р ИСО 10303–41. Ее формализованное описание на языке Express (ГОСТ Р ИСО 10303–11) приведено в А.1.

    2.  Тип (уникальное наименование) свойства описывается ИО **general_property** (рисунок 1). Данный ИО описывает тип свойства (например, «шероховатость поверхности») независимо от того объекта, который может обладать данным свойством.

<img src="standards/77-304/media/media/image2.png" style="width:6.69306in;height:3.52292in" />

1.  Совокупность ИО, описывающих свойства объекта

    1.  Между двумя типами свойств могут быть установлены связи (ИО **general_property_relationship**). Тип связи определяется для конкретного контекста применения. Например, это может быть связь между общим свойством и конкретным показателем, его определяющим (например, безотказность – параметр потока отказов).

    2.  С использованием ИО **general_property_association** устанавливается связь между типом свойства (атрибут «base_definition») и конкретным свойством (атрибут «derived_definition») конкретного объекта (ИО **property_definition**).

    3.  ИО **property_definition** описывает свойство, характеризующее конкретный объект («definition»). Наименование каждого конкретного свойства может быть определено либо его связью с типом свойства, либо его атрибутом» «name».

    4.  ИО **product_definition_shape** — это подтип ИО **property_definition** – свойство, определяющее форму объекта.

Примечания

1 ИО Product_definition_shape не обязательно должен быть связан с каким-либо геометрическим представлением.

2\. На начальном этапе проектирования продукта может отсутствовать конкретная идея о форме изделия, но могут быть определены необходимые характеристики формы (например, изделие должно помещаться в куб с длиной ребра 5 см). Эти характеристики формы можно связать с изделием с помощью данного ИО.

5.  Свойство объекта должно быть связано с самим объектом. Для установления такой связи используется атрибут «definition» ИО **property_definition**. Этот атрибут может ссылаться на один из следующих ИО:

-   shape_aspect;

-   characterized_object;

-   product_definition_relationship;

-   product_definition;

-   product_definition_occurence.

6.  <span id="_Toc224213440" class="anchor"></span>Значения свойств

    1.  Правила указания значений свойств основаны на схеме данных product_property_representation_schema, установленной в ГОСТ Р ИСО 10303–41. Ее формализованное описание на языке Express (ГОСТ Р ИСО 10303-11) приведено в А.2. Ниже приводится описание применения данной схемы для представления свойств изделий машиностроения и их СЧ.

    2.  Значение свойства задаются путем установления связи свойства объекта (конкретного типа) с «представлением», описывающим конкретное значение этого свойства.

В общем случае с одним свойством объекта может быть связано множество представлений, представляющих значения данного свойства в разных контекстах. А также одно представления может использоваться как значение для множества свойств (как правило, одного определенного типа) разных объектов.

3.  ИО **property_definition_representation** (рисунок 2) описывает связь между свойством (см. раздел 5) (атрибут «definition») и представлением этого свойства (атрибут «used_representation»).

Примечание – Общая схема данных для формирования «представления» (ИО **representation**) описана в разделе 7, но применяется в данном разделе.

<img src="standards/77-304/media/media/image3.png" style="width:6.69306in;height:4.62917in" />

2.  Совокупность ИО, описывающих значения свойств

    1.  Если свойство связано с формой объекта, то используется подтип ИО **shape_definition_representation**, который в атрибуте «used_representation» ссылается на представление формы (ИО **shape_representation** – см. раздел 7).

    2.  Если форма объекта зависит от его применения в структуре другого изделия (например, материал в сборочной единице), то используется ИО **context_dependent_shape_representation** (рисунок 3). Данный ИО устанавливает связь между ИО **shape_representation_relationship** (связь между двумя формами объектов) и ИО **product_definition_shape** (указывает на связь между двумя объектами в составе сборки, в контексте которой определена форма объекта).

Атрибут «rep_2» ИО **shape_representation_relationship** определяет форму объекта, который задает контекст. Атрибут «rep_1» ИО **shape_representation_relationship** определяет форму объекта, чья форма зависит от применения в другом объекте.

<img src="standards/77-304/media/media/image4.png" style="width:6.69306in;height:4.13333in" />

3.  Совокупность ИО, описывающих форму объекта в контексте другого объекта

Примечание – ISO 10303 использует методологию построения гибридных структур изделий (негеометрических) и (геометрических) моделей сборок, которые связывают тензорное преобразование жесткого тела для размещения геометрических моделей деталей в геометрической модели сборки. Эти гибридные структуры разлагают связь с преобразованием и само преобразование на отдельные EXPRESS-конструкции; однако они спроектированы и интегрированы для функционирования как единой модели.

7.  <span id="_Toc224213441" class="anchor"></span>Представления

## 7.1 Общие сведения о представлениях

7.1.1 Правила использования представлений в информационной модели основаны на схеме данных representation_schema, установленной в  
ГОСТ Р ИСО 10303–43. Ее формализованное описание на языке Express  
(ГОСТ Р ИСО 10303-11) приведено в А.2. Ниже приводится описание применения данной схемы для представления свойств изделий машиностроения и их СЧ.

7.1.2 Представление – универсальное понятие в ГОСТ Р ИСО 10303, используемое для описания свойств объектов, в том числе изделий. ИО **representation** (рисунок 4) формирует совокупность взаимосвязанных ИО **representation_item** (элементов представления), организованных определенным образом.

ИО **representation** (и его подтипы) используются для структурированного представления информации о форме изделия, требования к точности изготовления, требования к шероховатости поверхностей, для графического отображения информации о размерах и т. п.

7.1.3 Структура ИО **representation** не зависит от аспекта (способа) его использования, при этом одно представление может быть частью другого представления. Также преставления могут быть связаны иными типами связей.

7.1.4 Каждое представление имеет связь с контекстом, для которого оно определено (ИО **representation_context**). Все элементы представления (ИО **representation_item**) связаны между собой в указанном контексте.

7.1.5 Контекст представления может быть связан с другими контекстами.

Примечание — не все данные об изделии должны описываться с использованием представлений, а только те, которые имеют смысл в конкретном контексте. Например, «точка» – это элемент представления в контексте конкретного координатного пространства. При этом «имя человека» - имеет значение отдельно от любого контекста.

7.1.6 Элемент представления может входить в представление непосредственно или посредством связи с другими элементами представления.

Примечание – Кривая определяется несколькими точками. Все эти точки находятся в том же координатном пространстве, что и кривая, в силу их привязки к кривой.

7.1.7 Каждый элемент представления может входить в одно или несколько представлений.

Элементы представления считаются связанными, если:

\- они являются элементами одного и того же представления, или

\- они являются элементами разных представлений, которые имеют одинаковый контекст, или

\- это элементы в разных представлениях, которые имеют разные контексты, но эти контексты связаны.

Примечание – Пусть имеется две точки со значениями координат (0,0,0) и (1,0,0). Невозможно вычислить расстояние между этими точками, пока не будет установлено, что они находятся в одном координатном пространстве. Координаты точки сами по себе не содержат достаточно данных, чтобы указать, в каком координатном пространстве она находится и какие другие элементы также разделяют это координатное пространство. Точка является примером элемента представления, а координатное пространство - примером контекста представления.

| <img src="standards/77-304/media/media/image5.png" style="width:9.76378in;height:3.65748in" /> | Рисунок 4 – Совокупность ИО для формирования представления |
|------------------------------------------------------------------------------------------------|------------------------------------------------------------|

7.1.9 Представления, не связанные в одном контексте, могут быть связаны в другом.

Примечание – Форма каждой составной части сборочной единицы может быть представлена как независимое представление, не связанное с формой других составных частей. Однако в контексте собранной сборочной единицы формы составных частей взаимосвязаны.

7.1.10 Аспект данных об изделии может иметь ноль, одно или множество представлений, ни одно из которых не описывает изделие в полной (абсолютной) степени.

Примечание – Например, форма детали может быть представлена набором как двумерных геометрических данных, так и конструктивной твердотельной геометрией (constructive solid geometry). Любое представление является идеализацией формы.

Каждое представление не обязательно является полным описанием какого-либо аспекта данных об изделии, но оно может представлять модель, подходящую для конкретного применения.

## 7.2 Связи между представлениями и элементами представления

7.2.1 Представление может быть связано с другим представлением. Связь между представлениями также связывает их контексты.

Примечание – Например, расстояние между точками имеет смысл только в том случае, если системы координат, в которых эти точки определены, могут быть связаны между собой.

7.2.2 Одно представление может быть связано с другим представлением таким образом, что они оба участвуют в объединении, но одно не определяет другое. Этот тип связи соответствует ИО **representation_relationship** (рисунок 5).

7.2.3 Одно представление может быть связано с другим представлением таким образом, что первое является частью определения второго. Этот тип связи соответствует ИО **mapped_item** и ИО **representation_map**.

7.2.4 Две коллекции элементов представления могут находиться в двух отдельных, не связанных между собой контекстах и, тем не менее, быть связанными в третьем контексте или быть связанными только потому, что они оба участвуют в взаимосвязанной структуре.

Примечание – Например, форма двух разных деталей может быть описана в виде двух разных наборов точек и линий. Эти представления определены в разных контекстах, не связанных друг с другом. Для представления формы сборочной единицы, компонентами которой являются эти детали, определен третий контекст. В этом третьем контексте все элементы связаны посредством набора ассоциаций представления каждой составной части с представлением сборочной единицы.

7.2.5 Пара связанных с использованием агрегированной структуры ИО **representation_item** может быть включена в агрегированный набор элементов ИО **set_item_defined_transformation** в определенном преобразовании типа данных, которое задается ИО **representation_relationship_with_transformation**.

Примечание – Два представления содержат информацию о разных свойствах детали. Одно представление предназначено для описания функциональных свойств. Второе представление предназначено для описания геометрической формы. Функциональные свойства и свойства формы не связаны.

| <img src="standards/77-304/media/media/image6.png" style="width:9.84866in;height:2.97565in" /> | Рисунок 5 – Совокупность ИО, описывающих связи между представлениями |
|------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|

## 7.3 Преобразование элементов представления

7.3.1 Каждый элемент представления, входящий в состав одного представления, может быть преобразован в элемент представления в составе другого представлении с помощью одного преобразования.

Преобразование описывается ИО **representation_relationship_with\_ transformation** (см. рисунок 5), у которого атрибут transformation_operator указывает либо на ИО **item_defined_transformation** (неявное преобразование), либо на ИО **functionally_defined_transformation** (явное преобразование).

7.3.2 Элементы в разных представлениях могут сравниваться, если представления имеют одинаковый контекст или определено преобразование, которое связывает представления друг с другом.

7.3.3 Для полного определения преобразования требуется:

\- набор элементов **a** (ИО **representation_item**), подлежащих преобразованию;

\- набор элементов **b** (ИО **representation_item**), являющийся результатом преобразований;

\- определение контекста **A** (ИО **representation_context**.), который является общим для набора элементов **a**;

\- определение контекста **B** (ИО **representation_context.)**, который является общим для набора элементов **b**;

\- определение оператора преобразования (-\>).

7.3.4 Используются два разных подхода к определению операторов преобразования:

1\) оператор преобразования может быть указан явно. В этом случае используется оператор преобразования, соответствующий ИО **functionally_defined_transformation**.

Примечание – Два представления связаны таким образом, что одно из них повернуто и смещено относительно другого. Такое преобразование, может быть представлено матрицей.

2\) оператор преобразования может быть явно не указан. Можно указать элемент **a** в контексте **A** и элемент **b** в контексте **B**, и этого может быть достаточно для описания преобразования. Этот тип преобразования использует оператор преобразования в виде ИО **item_defined_transformation** или ИО **mapped_item**.

Примечание – Преобразование между координатными пространствами может быть однозначно определено двумя представлениями r1 и r2, двумя контекстами A и B (r1 ссылается на A, r2 ссылается на B) и двумя ИО **axis2_placement_3d** a1 и b1 (a1 в r1 и b1 в r2), так что оператор преобразования указывает a1 и b1. Принимающее приложение вычислило бы соответствующее преобразование из этой совокупности данных и применило бы его к каждому из элементов в r1, чтобы создать обновленную модель в памяти приложения.

## 7.4 Погрешность представления

7.1 Числовые значения, которые измеряются или рассчитываются, могут быть неточными. Погрешность может быть выражена через меру.

Мера погрешности может быть задана для:

\- нескольких представлений, которые имеют общий контекст;

\- отдельных представлений;

\- отдельных элементов представлений.

Примечание – Неточность не связана с допусками или допустимыми отклонениями.

В первом случае мера погрешности задается для числовых значений всех представлений, которые совместно используют один контекст, с использованием ИО **global_uncertainty_assigned_context**.

Во втором случае мера погрешности задается для числовых значений конкретного представления в данном контексте с использованием ИО **uncertainty_assigned_representation**.

7.2 Если меры погрешности указаны более одного раза, должны применяться следующие правила приоритета: погрешность, указанная для конкретного представления (ИО **uncertainty_assigned_representation**), должна иметь приоритет над погрешностью, указанной на уровне контекста (ИО **global_uncertainty_assigned_context**).

<span id="_Toc224213446" class="anchor"></span>Приложение А  
(справочное)  
Формализованное описание информационной модели на языке Express

## А.1 product_property_definition_schema

Настоящая схема является модифицированной версией одноименной схемы по ГОСТ Р ИСО 10303-41. Изменения включают удаление неиспользуемых в настоящем стандарте объектов и типов, а также исключение описания функций (с целью сокращения объема текста).

SCHEMA product_property_definition_schema '{iso standard 10303 part(41) version(10) object(1) product_property_definition_schema(19)}';

  TYPE characterized_definition = SELECT (

    characterized_object,

    characterized_product_definition,

    shape_definition);

  END_TYPE;

  TYPE characterized_product_definition = SELECT (

    product_definition,

    product_definition_occurrence,

    product_definition_relationship,

    product_definition_relationship_relationship);

  END_TYPE;

  TYPE derived_property_select = SELECT (

    property_definition,

  END_TYPE;

  TYPE shape_aspect_or_characterized_object = SELECT (shape_aspect, characterized_object);

  END_TYPE;

 

  TYPE shape_definition = SELECT (product_definition_shape, shape_aspect, shape_aspect_relationship);

  END_TYPE;

  TYPE internal_or_reflected_shape_aspect = SELECT (

    shape_aspect,

    identifier);

  END_TYPE;

  TYPE multi_or_next_assembly_usage_occurrence = SELECT (

    multi_level_reference_designator,

    next_assembly_usage_occurrence);

  END_TYPE;

  ENTITY characterized_object;

    name : label;

    description : OPTIONAL text;

  END_ENTITY;

  ENTITY characterized_object_relationship;

    name : label;

    description : OPTIONAL text;

    relating_object : characterized_object;

    related_object : characterized_object;

  END_ENTITY;

  ENTITY general_property;

    id : identifier;

    name : label;

    description : OPTIONAL text;

  END_ENTITY;

  ENTITY general_property_association;

    name : label;

    description : OPTIONAL text;

    base_definition : general_property;

    derived_definition : derived_property_select;

  END_ENTITY;

  ENTITY general_property_relationship;

    name : label;

    description : OPTIONAL text;

    relating_property : general_property;

    related_property : general_property;

  END_ENTITY;

  ENTITY product_definition_shape

    SUBTYPE OF (property_definition);

  UNIQUE

    UR1: SELF\\property_definition.definition;

  WHERE

    WR1: SIZEOF(\['PRODUCT_PROPERTY_DEFINITION_SCHEMA.CHARACTERIZED_PRODUCT_DEFINITION', 'PRODUCT_PROPERTY_DEFINITION_SCHEMA.CHARACTERIZED_OBJECT'\] \* TYPEOF(SELF\\property_definition.definition)) \> 0;

  END_ENTITY;

  ENTITY property_definition;

    name : label;

    description : OPTIONAL text;

    definition : characterized_definition;

  DERIVE

    id : identifier := get_id_value(SELF);

  WHERE

    WR1: SIZEOF(USEDIN(SELF, 'BASIC_ATTRIBUTE_SCHEMA.' + 'ID_ATTRIBUTE.IDENTIFIED_ITEM')) \<= 1;

  END_ENTITY;

  ENTITY shape_aspect

    SUPERTYPE OF (ONEOF (shape_aspect_occurrence, component_path_shape_aspect)

                  ANDOR constituent_shape_aspect);

    name : label;

    description : OPTIONAL text;

    of_shape : product_definition_shape;

    product_definitional : LOGICAL;

  DERIVE

    id : identifier := get_id_value(SELF);

  UNIQUE

    UR1: id, of_shape;    

  WHERE

    WR1: SIZEOF(USEDIN(SELF, 'BASIC_ATTRIBUTE_SCHEMA.' + 'ID_ATTRIBUTE.IDENTIFIED_ITEM')) \<= 1;

  END_ENTITY;

  ENTITY shape_aspect_occurrence

    SUBTYPE OF (shape_aspect);

    definition : shape_aspect_or_characterized_object;

  WHERE

    WR1: acyclic_shape_aspect_occurrence(SELF,definition);

  END_ENTITY;

END_SCHEMA;

## А.2 product_property_representation_schema

Настоящая схема является модифицированной версией одноименной схемы по ГОСТ Р ИСО 10303-41. Изменения включают удаление неиспользуемых в настоящем стандарте объектов и типов, а также исключение описания функций (с целью сокращения объема текста).

SCHEMA product_property_representation_schema '{iso standard 10303 part(41) version(10) object(1) product_property_representation_schema(20)}';

  REFERENCE FROM material_property_definition_schema (   -- ISO 10303-45

    property_definition_relationship);

  REFERENCE FROM product_definition_schema (   -- ISO 10303-41

    product_definition,

    product_definition_relationship);

  REFERENCE FROM product_property_definition_schema (   -- ISO 10303-41

    characterized_object,

    characterized_definition,

    general_property,

    product_definition_shape,

    property_definition,

    shape_aspect,

    shape_aspect_relationship);

  REFERENCE FROM product_structure_schema (  -- ISO 10303-44

    product_definition_specified_occurrence);

  REFERENCE FROM representation_schema (   -- ISO 10303-43

    representation,

    representation_item,

    representation_relationship,

    representation_reference,

    using_representations,

    mapped_item,

    representation_context,

    representation_map,

    list_representation_item,

    set_representation_item,

    get_representations_for_items);

  REFERENCE FROM support_resource_schema (   -- ISO 10303-41

    bag_to_set,

    label,

    text);

  TYPE pprs_description_attribute_select = SELECT BASED_ON description_attribute_select WITH (

    context_dependent_shape_representation,

    property_definition_representation);

  END_TYPE;

 

  TYPE pprs_name_attribute_select = SELECT BASED_ON name_attribute_select WITH (

    context_dependent_shape_representation,

    property_definition_representation);

  END_TYPE;

  TYPE chained_representation_link = SELECT (mapped_item, representation_context, representation_relationship);

  END_TYPE;

  TYPE represented_definition = SELECT (

    general_property,

    property_definition,

    property_definition_relationship,

    shape_aspect,

    shape_aspect_relationship);

  END_TYPE;

  TYPE item_identified_representation_usage_definition = EXTENSIBLE GENERIC_ENTITY SELECT (

    represented_definition);

  END_TYPE;

 

  TYPE item_identified_representation_usage_select = SELECT (

    representation_item,

    list_representation_item,

    set_representation_item);

  END_TYPE;  

  ENTITY characterized_item_within_representation

    SUBTYPE OF (characterized_object);

    item : representation_item;

    rep : representation;

  UNIQUE

    UR1: item, rep;

  WHERE

    WR1: rep IN using_representations(item);

  END_ENTITY;

  ENTITY context_dependent_shape_representation;

    representation_relation : shape_representation_relationship;

    represented_product_relation : product_definition_shape;

  DERIVE

    description : text := get_description_value(SELF);

    name : label := get_name_value(SELF);

  WHERE

    WR1: 'PRODUCT_DEFINITION_SCHEMA.PRODUCT_DEFINITION_RELATIONSHIP' IN TYPEOF(represented_product_relation\\property_definition.definition);

    WR2: SIZEOF(USEDIN(SELF, 'BASIC_ATTRIBUTE_SCHEMA.' + 'DESCRIPTION_ATTRIBUTE.DESCRIBED_ITEM')) \<= 1;

    WR3: SIZEOF(USEDIN(SELF, 'BASIC_ATTRIBUTE_SCHEMA.' + 'NAME_ATTRIBUTE.NAMED_ITEM')) \<= 1;

  END_ENTITY;

  ENTITY property_definition_representation;

    definition : represented_definition;

    used_representation : representation;

  DERIVE

    description : text := get_description_value(SELF);

    name : label := get_name_value(SELF);

  WHERE

    WR1: SIZEOF(USEDIN(SELF, 'BASIC_ATTRIBUTE_SCHEMA.' + 'DESCRIPTION_ATTRIBUTE.DESCRIBED_ITEM')) \<= 1;

    WR2: SIZEOF(USEDIN(SELF, 'BASIC_ATTRIBUTE_SCHEMA.' + 'NAME_ATTRIBUTE.NAMED_ITEM')) \<= 1;

  END_ENTITY;

  ENTITY shape_definition_representation

    SUBTYPE OF (property_definition_representation);

    SELF\\property_definition_representation.definition : property_definition;

    SELF\\property_definition_representation.used_representation : shape_representation;

  WHERE

    WR1: ('PRODUCT_PROPERTY_DEFINITION_SCHEMA.PRODUCT_DEFINITION_SHAPE' IN TYPEOF(definition)) OR

         ('PRODUCT_PROPERTY_DEFINITION_SCHEMA.SHAPE_DEFINITION' IN TYPEOF(definition\\property_definition.definition));  

  END_ENTITY;

  ENTITY shape_representation

    SUBTYPE OF (representation);

  END_ENTITY;

  ENTITY shape_representation_relationship

    SUBTYPE OF (representation_relationship);

  WHERE

    WR1: SIZEOF(\['PRODUCT_PROPERTY_REPRESENTATION_SCHEMA.SHAPE_REPRESENTATION',

                 'PRODUCT_PROPERTY_REPRESENTATION_SCHEMA.SHAPE_REPRESENTATION_REFERENCE'\] \*

               (TYPEOF( SELF\\representation_relationship.rep_1 ) +

                TYPEOF( SELF\\representation_relationship.rep_2 ) ) )

               \>= 1;

  END_ENTITY;

  ENTITY specified_occurrence_context_dependent_shape_representation

    SUBTYPE OF (context_dependent_shape_representation);

    sub_element : product_definition_specified_occurrence;

  WHERE

    WR1: 'PRODUCT_DEFINITION_SCHEMA.PRODUCT_DEFINITION_OCCURRENCE' IN TYPEOF(SELF.represented_product_relation.definition.related_product_definition);

    WR2: sub_element IN represented_product_relation.definition.related_product_definition.descendant_occurrences;

  END_ENTITY;

END_SCHEMA;

## А.3 representation_schema

Настоящая схема является модифицированной версией одноименной схемы по ГОСТ Р ИСО 10303-43. Изменения включают удаление неиспользуемых в настоящем стандарте объектов и типов, а также исключение описания функций (с целью сокращения объема текста).

SCHEMA representation_schema '{iso standard 10303 part(43) version(7) object(1) representation_schema(1)}';

REFERENCE FROM basic_attribute_schema   -- ISO 10303-41

  (description_attribute, description_attribute_select, get_description_value,

   get_id_value, id_attribute, id_attribute_select);

REFERENCE FROM measure_schema   -- ISO 10303-41

  (measure_value, measure_with_unit);

REFERENCE FROM support_resource_schema   -- ISO 10303-41

  (bag_to_set, identifier, label, text);

   

  TYPE compound_item_definition = SELECT

    (list_representation_item, set_representation_item);

  END_TYPE;

  TYPE transformation = SELECT

    (item_defined_transformation, functionally_defined_transformation,

     set_item_defined_transformation);

  END_TYPE;

  ENTITY binary_representation_item

    SUBTYPE OF (representation_item);

      binary_value : BINARY;

  END_ENTITY;

  ENTITY bytes_representation_item

    SUBTYPE OF (binary_representation_item);

    DERIVE

      no_of_bytes : INTEGER := BLENGTH(SELF\\binary_representation_item.binary_value) DIV 8;

    WHERE

      WR1: BLENGTH(SELF\\binary_representation_item.binary_value) MOD 8 = 0;

  END_ENTITY;

  ENTITY compound_representation_item

    SUBTYPE OF (representation_item);

      item_element : compound_item_definition;

  END_ENTITY;

  ENTITY definitional_representation

    SUBTYPE OF (representation);

    WHERE

      WR1: 'REPRESENTATION_SCHEMA.PARAMETRIC_REPRESENTATION_CONTEXT' IN

          TYPEOF (SELF\\representation.context_of_items );

  END_ENTITY;

  ENTITY definitional_representation_relationship

    SUBTYPE OF (representation_relationship);

     WHERE

       WR1: acyclic_representation_relationship(SELF,

         \[SELF\\representation_relationship.rep_2\],

         'REPRESENTATION_SCHEMA.'+'REPRESENTATION');

  END_ENTITY;  

  ENTITY definitional_representation_relationship_with_same_context

    SUBTYPE OF (definitional_representation_relationship);

     WHERE

       WR1: SELF\\representation_relationship.rep_1.context_of_items :=:

            SELF\\representation_relationship.rep_2.context_of_items;

  END_ENTITY;  

  ENTITY functionally_defined_transformation;

    name        : label;

    description : OPTIONAL text;

  END_ENTITY;

  ENTITY global_uncertainty_assigned_context

    SUBTYPE OF (representation_context);

      uncertainty : SET \[1:?\] OF uncertainty_measure_with_unit;

  END_ENTITY;

  ENTITY item_defined_transformation;

    name             : label;

    description      : OPTIONAL text;

    transform_item_1 : representation_item;

    transform_item_2 : representation_item;

  END_ENTITY;

  ENTITY mapped_item

    SUBTYPE OF (representation_item);

      mapping_source : representation_map;

      mapping_target : representation_item;

    WHERE

      WR1: acyclic_mapped_representation(SELF);

  END_ENTITY;

  ENTITY parametric_representation_context

    SUBTYPE OF (representation_context);

  END_ENTITY;

  ENTITY representation;

      name             : label;

      items            : SET\[1:?\] OF representation_item;

      context_of_items : representation_context;

    DERIVE

      id               : identifier := get_id_value (SELF);

      description      : text := get_description_value (SELF);

    WHERE

      WR1: SIZEOF (USEDIN (SELF, 'BASIC_ATTRIBUTE_SCHEMA.' +

                                 'ID_ATTRIBUTE.IDENTIFIED_ITEM'))

         \<= 1;

      WR2: SIZEOF (USEDIN (SELF, 'BASIC_ATTRIBUTE_SCHEMA.' +

                                 'DESCRIPTION_ATTRIBUTE.DESCRIBED_ITEM'))

         \<= 1;

  END_ENTITY;

  ENTITY representation_context;

      context_identifier : identifier;

      context_type       : text;

    INVERSE

      representations_in_context : SET \[1:?\] OF representation FOR context_of_items;

  END_ENTITY;

  ENTITY representation_item

    SUPERTYPE OF(ONEOF(binary_representation_item,

      compound_representation_item,

      mapped_item,

      value_representation_item));

      name : label;

    WHERE

      WR1: SIZEOF(using_representations(SELF)) \> 0;

  END_ENTITY;

  ENTITY representation_item_relationship;

    name : label;

    description : OPTIONAL text;

    relating_representation_item : representation_item;

    related_representation_item : representation_item;

  END_ENTITY;

  ENTITY representation_map;

      mapping_origin        : representation_item;

      mapped_representation : representation;

    INVERSE

      map_usage : SET\[1:?\] OF mapped_item FOR mapping_source;

    WHERE

      WR1: item_in_context(mapping_origin, mapped_representation\\representation.context_of_items);

  END_ENTITY;

  ENTITY representation_relationship;

      name        : label;

      description : OPTIONAL text;

      rep_1        : representation_or_representation_reference;

      rep_2        : representation_or_representation_reference;

  END_ENTITY;

  ENTITY representation_relationship_with_transformation

    SUBTYPE OF (representation_relationship);

      transformation_operator : transformation;

    WHERE

      WR1: SELF\\representation_relationship.rep_1.context_of_items

           :\<\>: SELF\\representation_relationship.rep_2.context_of_items;

      WR2: NOT('REPRESENTATION_SCHEMA.ITEM_DEFINED_TRANSFORMATION' IN TYPEOF(transformation_operator)) OR

              (SELF\\representation_relationship.rep_1 IN

               using_representations(transformation_operator\\item_defined_transformation.transform_item_1)) AND

              (SELF\\representation_relationship.rep_2 IN

               using_representations(transformation_operator\\item_defined_transformation.transform_item_2));

  END_ENTITY;

  ENTITY uncertainty_assigned_representation

    SUBTYPE OF (representation);

      uncertainty : SET \[1:?\] OF uncertainty_measure_with_unit;

  END_ENTITY;

  ENTITY uncertainty_measure_with_unit

    SUBTYPE OF (measure_with_unit);

      name        : label;

      description : OPTIONAL text;

    WHERE

      WR1: valid_measure_value (SELF\\measure_with_unit.value_component);

  END_ENTITY;

  ENTITY value_representation_item

    SUBTYPE OF (representation_item);

      value_component : measure_value;

    WHERE

      WR1: SIZEOF (QUERY (rep \<\* using_representations (SELF) \|

        NOT ('MEASURE_SCHEMA.GLOBAL_UNIT_ASSIGNED_CONTEXT'

        IN TYPEOF (rep.context_of_items)

        ))) = 0;

  END_ENTITY;

| УДК 006.1:006.354 ОКС 35.240.50                                                                    |
|----------------------------------------------------------------------------------------------------|
| Ключевые слова: изделие, свойство изделия, представление свойства, элемента представления свойства |

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 28%" />
<col style="width: 21%" />
</colgroup>
<thead>
<tr class="header">
<th><p>Руководитель организации-разработчика</p>
<p>АО НИЦ «Прикладная логистика»,</p>
<p>Генеральный директор</p></th>
<th></th>
<th>И.Ю. Галин</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td><p>Руководитель разработки,</p>
<p>руководитель отдела НО</p></td>
<td></td>
<td>Е.В. Селезнёва</td>
</tr>
<tr class="odd">
<td></td>
<td></td>
<td></td>
</tr>
<tr class="even">
<td><p>Разработчик стандарта,</p>
<p>руководитель центра</p>
<p>перспективных разработок</p></td>
<td></td>
<td>Д.Н. Бороздин</td>
</tr>
</tbody>
</table>

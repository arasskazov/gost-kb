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
<td><img src="standards/77-305/media/media/image1.png" style="width:1.42708in;height:0.89583in" /></td>
<td></td>
<td><p><strong>НАЦИОНАЛЬНЫЙ</strong></p>
<p><strong>СТАНДАРТ</strong></p>
<p><strong>РОССИЙСКОЙ</strong></p>
<p><strong>ФЕДЕРАЦИИ</strong></p></td>
<td></td>
<td><p><strong>ГОСТ Р</strong></p>
<p><strong>77.305―</strong></p>
<p><strong>202Х</strong></p>
<p><em>(проект, первая<br />
редакция)</em></p></td>
</tr>
</tbody>
</table>

**Система поддержки жизненного цикла изделия**

**ИНФОРМАЦИОННАЯ МОДЕЛЬ ИЗДЕЛИЯ**

**Материалы и их свойства**

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

[4 Общие положения](#_Toc224213850)

[5 Идентификация материала](#_Toc224213851)

[6 Представление свойства материала](#_Toc224213852)

[7 Задание количественных характеристик](#_Toc224213853)

[Приложение А (справочное) Формализованное описание информационной модели на языке Express](#_Toc224213854)

**НАЦИОНАЛЬНЫЙ СТАНДАРТ российской федерации**

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>Система поддержки жизненного цикла изделия</strong></p>
<p><strong>ИНФОРМАЦИОННАЯ МОДЕЛЬ ИЗДЕЛИЯ</strong></p>
<p><strong>Материалы и их свойства</strong></p>
<p>Product life cycle support system. Product information model.</p>
<p>Materials and material properties</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**Дата введения ―**

1.  <span id="_Toc445998457" class="anchor"></span>Область применения

Настоящий стандарт определяет составную часть интегрированной схемы данных, используемой для создания и применения информационной модели изделия машиностроения. В стандарте установлены правила описания материалов и свойств материалов, используемых для изготовления деталей, материалов для полуфабрикатов и заготовок.

2.  <span id="_Toc467869760" class="anchor"></span>Нормативные ссылки

В настоящем стандарте использованы нормативные ссылки на следующие стандарты:

ГОСТ Р 2.005  Единая система конструкторской документации. Термины и определения

ГОСТ Р 2.101  Единая система конструкторской документации. Виды изделий

ГОСТ Р 77.002  Система поддержки жизненного цикла изделия. Термины и определения *(проект, окончательная редакция, разрабатывается совместно)*

ГОСТ Р 77.301  Система поддержки жизненного цикла изделия. Информационная модель изделия. Основные положения *(проект, первая редакция, разрабатывается совместно)*

ГОСТ Р 77.304  Система поддержки жизненного цикла изделия. Информационная модель изделия. представление свойств *(проект, первая редакция, разрабатывается совместно)*

ГОСТ Р ИСО 10303–11 Системы автоматизации производства и их интеграция. Представление данных об изделии и обмен этими данными. Часть 11. Методы описания. Справочное руководство по языку EXPRESS

ГОСТ Р ИСО 10303–45 Системы автоматизации производства и их интеграция. Представление данных об изделии и обмен этими данными. Часть 45. Интегрированный обобщенный ресурс. Материал и другие технические характеристики

Примечание  При пользовании настоящим стандартом целесообразно проверить действие ссылочных стандартов в информационной системе общего пользования – на официальном сайте Федерального агентства по техническому регулированию и метрологии в сети Интернет или по ежегодному информационному указателю «Национальные стандарты», который опубликован по состоянию на 1 января текущего года, и по выпускам ежемесячного информационного указателя «Национальные стандарты» за текущий год. Если заменен ссылочный стандарт, на который дана недатированная ссылка, то рекомендуется использовать действующую версию этого стандарта с учетом всех внесенных в данную версию изменений. Если заменен ссылочный стандарт, на который дана датированная ссылка, то рекомендуется использовать версию этого стандарта с указанным выше годом утверждения (принятия). Если после утверждения настоящего стандарта в ссылочный стандарт, на который дана датированная ссылка, внесено изменение, затрагивающее положение, на которое дана ссылка, то это положение рекомендуется применять без учета данного изменения. Если ссылочный стандарт отменен без замены, то положение, в котором дана ссылка на него, рекомендуется применять в части, не затрагивающей эту ссылку.

3.  <span id="_Toc467869761" class="anchor"></span>Термины, определения и сокращения

3.1 В настоящем стандарте применены термины по ГОСТ Р 2.005 и ГОСТ Р 77.002, а также термин:

3.1.1 **схема данных:** Формальное описание организации данных, в том числе описание элементов данных, взаимосвязей между ними, типов данных, возможных значений и ограничений.

3.2 В настоящем стандарте применены следующие сокращения:

| ЕСКД | —   | единая система конструкторской документации; |
|------|-----|----------------------------------------------|
| ИО   | —   | информационный объект;                       |
| СПЖЦ | —   | система поддержки жизненного цикла изделий.  |

4.  <span id="_Toc224213850" class="anchor"></span>Общие положения

    1.  Установленные настоящим стандартом схемы данных базируются не схемах ГОСТ Р ИСО 10303-45:

        \- material_property_definition_schema;

        \- material_property_representation \_schema;

        \- qualified_measure_schema.

    2.  Приведенные в настоящем стандарте схемы данных позволяют описывать материалы, используемые для изготовления деталей, материалы для полуфабрикатов и заготовок. Схемы данных адаптированы с учетом терминологии и требований стандартов ЕСКД и могут быть использованы для представления данных об изделиях машиностроения и их СЧ, разрабатываемых в соответствии со стандартами ЕСКД.

        Примечание — В настоящем стандарте для представления схем данных используется текстовое представление по ГОСТ Р ИСО 10303-11. Для пояснений также используются графические схемы в нотации, установленной в ГОСТ Р 77.301.

4.3. Приведенные в стандарте схемы данных обеспечивают представление следующей информации:

\- идентификация материала;

\- свойства материала и характеристики, выражающие свойства;

\- методики (процедуры) получения значений характеристик;

\- связи материала (свойства) с изделием, сведения о возможных вариантах;

\- внутренняя структура материала;

\- источники сведений о материале.

4.4 Идентификационная информация об изделии включает в себя обозначение и наименование материала в соответствии со стандартом или техническими документами поставщика (например, техническими условиями). Эти сведения могут быть указаны явно или путем ссылки на нормативный или иной технический документ.

4.5 Информация о свойствах материала задается через определение свойства материала и набор характеристик, выражающих данное свойство. Характеристики могут быть выражены числовыми значениями, наборами числовых значений, функциями, выражающими, зависимость значений характеристики от разных параметров и внешних факторов. Для числовых значений указываются единицы измерения, допустимые диапазоны значений, допуски и другая информация.

Примечание – Примерами характеристик свойств материала являются: предел прочности, плотность, теплопроводность диэлектрическая прочность и др.

4.6 Для свойства материала могут быть указаны метод испытаний или стандарт, определяющий процедуру, по которой получено заданное значение.

4.7 При описании материала и его свойств может быть указано как материал и его свойства связаны с элементами детали или с отдельными поверхностями детали (в случае покрытий), какие материалы (материалы с какими свойствами) использованы при изготовлении вариантов (исполнений) изделия или экземпляров (партий) изделий.

4.8 При описании материала могут быть приведены сведения о его внутренней структуре. Структура может быть:

\- однородная по составу и изотропная по свойствам (например, заготовка из металлического порошка, полученная спеканием);

\- неоднородная по составу и изотропная по свойствам (например, композиционный полимерный материал, полученный формованием);

\- однородная по составу и анизотропная по свойствам (например, лист, полученный прокатом из сплава);

\- неоднородная по составу и анизотропная по свойствам (например, пластина, изготовленная из армированного волокном полимерного композита).

4.9 Информационная модель, сформированная с использованием настоящей схемы данных, может использоваться:

\- для передачи данных из систем автоматизированного проектирования в системы инженерного анализа;

\- для обеспечения прослеживаемости свойств материалов на стадиях ЖЦ изделия и проверки соответствия заданным требованиям;

\- в составе цифрового двойника изделия.

4.10 Ниже приведены примеры описания материалов и их свойств в соответствии со схемой данных, установленной настоящим стандартов.

Примечание – Примеры сущностей, которые могут быть описаны с использованием схемы данных

1 Болт из стали 40Х: материал — «40Х по ГОСТ …», Свойства: плотность 7,85 г/см³, предел прочности 800 МПа при 20 °C по методу ISO …, твёрдость 28–32 HRC.

2 Пластик для корпуса изделия: модуль продольной упругости в виде таблицы значений функции «напряжение‑деформация» при температуре 23 °C и скорости деформации 0,01 с⁻¹.

3 Теплообменник: теплопроводность материала в виде зависимости λ(T) от температуры (в диапазоне −40 до 200 °C в табличном представлении.

4 Печатная плата: электрическая прочность диэлектрика и тангенс δ на частотах 1, 10 и 100 кГц с привязкой к конкретным слоям стеклотекстолита.

5 Покрытие: никелевое покрытие толщиной 12–15 мкм на заданных поверхностях детали, с указанием метода контроля толщины.

6 Детали, для которых для каждого экземпляра (серийного номера) указаны измеренные значения твёрдости и зернистости, с указанием методики измерения.

5.  <span id="_Toc224213851" class="anchor"></span>Идентификация материала

5.1 Правила идентификации материалов основаны на схеме material_property_definition_schema, установленной в ГОСТ Р ИСО 10303–45. Ее формализованное описание на языке Express (ГОСТ Р ИСО 10303-11) приведено в А.1.

5.2 Для идентификации материала используются следующие основные ИО (рисунок 1):

\- **material_designation** –обозначение материала;

\- **material_designation_characterization** – наименование (назначение) материала.

<img src="standards/77-305/media/media/image2.png" style="width:5.42265in;height:3.76524in" />

Рисунок 1 – Основные ИО используемые для описания материала

5.3 ИО **material_designation** в атрибуте «name» определяет обозначение материала, например, «Сталь 40Х» или «Пластик ABS».

Обозначения материалов указываются в соответствии с документами по стандартизации или техническими документами поставщика (например, техническими условиями). При этом в атрибуте «definitions» можно указать одно или множество изделий или элементов изделий, для которых применяется данный материал (ИО **characterized_definition** описан в ГОСТ Р 77.304).

5.4 ИО **material_designation_characterization** устанавливает связь обозначения материала с его свойствами.

Обозначение материала, указанное в атрибуте «designation», связывается со свойством, указанным в атрибуте «property».

Свойства материала могут представлены при помощи ИО двух типов:

\- **material_property_representation –** описание свойства (более подробно рассмотрено в разделе 6);

\- **product_material_composition_relationship** – описание структуры материала (см. 5.6).

5.6 При описании структуры материала, например, сплава или композита с указанием количества слоев и их взаимного расположения, используется ИО **product_material_composition_relationship** (рисунок 2), являющийся подтипом ИО **product_definition_relationship.**

ИО **product_material_composition_relationship** связывает элемент структуры материала с изделием.

Изделие указывается в атрибуте «relating_product_definition», элемент структуры материала – в атрибуте – «related_product_definition».

Примечание – Пространственное расположение и ориентация компонентов материала в изделии (структура материала) определяются экземпляром ИО **product_definition_shape**.

<img src="standards/77-305/media/media/image3.png" style="width:3.53048in;height:3.83652in" />

Рисунок 2 – ИО используемые при описании структуры материала

В атрибуте *«*class» указывается название или идентификатор типа связи между элементом структуры материала и изделием, например, «смесь», «химически связанный» и «легированный».

В атрибуте «composition_basis» – указывается база для количественного анализа, например, «объем», «вес», «моли» и «атомы».

В атрибуте «determination_method» приводится описание процедуры определения количества.

В атрибуте «constituent_amount» указывается количество материала в изделии (с единицей величины). Количество может быть выражено как минимальное, максимальное или стандартное значение, в соответствии со схемой данных, приведенной в разделе 7.

6.  <span id="_Toc224213852" class="anchor"></span>Представление свойства материала

6.1 Правила представления свойств материала основаны на схеме material_property_representation \_schema, установленной в ГОСТ Р ИСО 10303–45. Ее формализованное описание языке Express (ГОСТ Р ИСО 10303-11) приведено в А.2.

6.2 Схема material_property_representation_schema предназначена для структурированного представления свойств материалов (механических, химических, физических) и связанных с ними условий (обеспечения, измерения).

6.3 Для представления свойств материала используются следующие основные ИО (рисунок 3):

\- **material_property** – определенное свойство материала;

\- **material_property_representation** – представление значения свойства;

\- **data_environment** – условия.

6.4 ИО **material_property** описывает свойство материала (например, плотность, прочность, теплопроводность) и является подтипом базового ИО **property_definition** (см. ГОСТ Р 77.304). Для описания взаимосвязи между различными свойствами материала или при выражении одного свойства через другое используется ИО **property_definition_relationship**.

6.5 ИО **material_property_representation** — описывает представление значения свойства (числовое значение, таблица, функция) с указанием условий, при выполнении которых данное значение свойства действительно.

6.6 Значение свойства может быть присвоено (задано) или измерено. Если значение измерено, то полученного значение могут быть указаны методы и условия измерения. Если значение присвоено, то могут быть указаны условия, при которых это значение свойства является действительным.

6.7 ИО **material_property_representation** это подтип ИО **property_definition_representation**, описанного в ГОСТ Р 77.304 и позволяющего к значению свойства добавить ссылку на условия (data_environment), при которых данное значение свойства действительно.

<img src="standards/77-305/media/media/image4.png" style="width:6.78427in;height:4.41031in" />

Рисунок 3 – ИО, используемые при описании свойств

6.8 Значения свойств могут быть выражены количественно (числовыми значениями) или качественно с помощью описания.

Пример– Условия окружающей среды для измерения могут быть выражены как “воздух в помещении” (качественное состояние) или воздух 20 градусов Цельсия и давление в 1 атмосферу.

6.9 ИО **data_environment** — ИО, описывающий условие, параметры среды или другие факторы, влияющие на свойства материала (температура, давление, влажность и т.д.). Каждое условие описывается с использованием ИО **property_definition_representation** или ИО **dimensional_characteristic_representation.**

Значение свойства материала **material_property_representation** справедливо только при выполнении определённых условий, описываемых ИО **data_environment.**

Условия могут быть комплексными. Для их описания используется ИО **data_environment_relationship,** который позволяет задавать отношения между экземплярами ИО **data_environment** и описывать комплексные условия, : например, «при температуре 20°C и влажности 50%».

7.  <span id="_Toc224213853" class="anchor"></span>Задание количественных характеристик

7.1 Правила описания количественных характеристик материала основаны на схеме qualified_measure_schema, установленной в ГОСТ Р ИСО 10303-45. Ее формализованное описание на языке Express (ГОСТ Р ИСО 10303-11) приведено в А.3.

Основная задача данной схемы данных — дополнить представление физических величин атрибутами, позволяющими указывать тип значения (измеренное, номинальное, максимальное и т.д.), количество значащих цифр, степень неопределенности и доверительные интервалы для измеряемых или вычисляемых величин.

Примечание – Nакие атрибуты, уточняющие значение величин, называются квалификаторами.

Схема qualified_measure_schema дополняет конструкции из measure_schema для обеспечения возможности задания количественных характеристик свойств и разрешенных формаов числовых значений.

7.3 В данной схеме и используются следующие основные ИО (4):

\- **qualified_representation_item** — ИО, содержащий набор квалификаторов;

\- **measure_qualification** — ИО, описывающий связь между конкретным измерением (**measure_with_unit**) и набором квалификаторов, что позволяет дополнять результат измерения подробностями о типе, точности и неопределенности (ошибке);

\- **value_qualifier** — квалификатор значения, имеет три варианта: precision_qualifier, type_qualifier, uncertainty_qualifier;

\- **type_qualifier** — квалификатор, указывающий тип значения: “measured” - измеренный, “nominal”- номинальный, “maximum” - максимальный, “design allowable”- допустимый конструкцией и другие;

\- **precision_qualifier** — задаёт количество значащих цифр при представлении значения;

\- **uncertainty_qualifier** — квалификатор погрешности (стандартная, качественная, интервальная) и способы расчета.

<img src="standards/77-305/media/media/image5.png" style="width:6.69306in;height:3.0125in" />

Рисунок 4 – ИО, используемые при задании количественных характеристик

Примеры

а) описание характеристик материала в форме: предел прочности (measured), представленное с точностью до 2 знаков, с интервальной неопределённостью, указывающей диапазон достоверности в 95%;.

б) представление расчетных параметров при моделировании: номинальное расчетное давление с указанием типа (“calculated”) и стандартной неопределенности, что важно для сравнения и сертификации.

в) передача сведений об изделиях в машиностроении: масса компонента описана квалификаторами “measured”, “maximum” и точностью (число знаков), что позволяет обеспечить сравнение изделий разных производителей.

<span id="_Toc224213854" class="anchor"></span>Приложение А  
(справочное)  
Формализованное описание информационной модели на языке Express

## А.1 material_property_definition_schema

Настоящая схема является модифицированной версией одноименной схемы по ГОСТ Р ИСО 10303-45. Изменения включают удаление неиспользуемых в настоящем стандарте объектов и типов

SCHEMA material_property_definition_schema '{iso standard 10303 part(45) version(4) object(1) material_property_definition_schema(1)}';

REFERENCE FROM material_property_representation_schema

     (material_property_representation);

REFERENCE FROM measure_schema

     (measure_with_unit);

REFERENCE FROM product_definition_schema

      (product_definition_relationship);

REFERENCE FROM product_property_definition_schema

      (characterized_definition,

      property_definition);

REFERENCE FROM qualified_measure_schema

     (maths_value_with_unit);

REFERENCE FROM support_resource_schema

     (label,

      text,

      bag_to_set);

TYPE characterized_material_property = SELECT

  (material_property_representation,

   product_material_composition_relationship);

END_TYPE;

ENTITY generic_property_relationship;

  name              : label;

  description       : text;

  relating      : generic_property_definition_select;

  related       : generic_property_definition_select;

  relation_type : STRING;

 WHERE

  WR1: acyclic_generic_property_relationship (SELF, \[related\], 'MATERIAL_PROPERTY_DEFINITION_SCHEMA.GENERIC_PROPERTY_RELATIONSHIP');

END_ENTITY;

ENTITY material_designation;

  name          : label;

  definitions   : SET \[1:?\] OF characterized_definition;

END_ENTITY;

ENTITY material_designation_characterization;

  name          : label;

  description   : text;

  designation   : material_designation;

  property      : characterized_material_property;

END_ENTITY;

ENTITY material_property

SUBTYPE OF (property_definition);

UNIQUE

  UR1 : SELF\\property_definition.name, SELF\\property_definition.definition;

WHERE

  WR1 : ('PRODUCT_PROPERTY_DEFINITION_SCHEMA.CHARACTERIZED_OBJECT' IN

          TYPEOF(SELF\\property_definition.definition)) OR

       (SIZEOF(bag_to_set(USEDIN(SELF ,

                     'PRODUCT_PROPERTY_REPRESENTATION_SCHEMA.' +

                     'PROPERTY_DEFINITION_REPRESENTATION.DEFINITION')) -

              QUERY(temp \<\* bag_to_set(USEDIN(SELF ,

                       'PRODUCT_PROPERTY_REPRESENTATION_SCHEMA.' +

                       'PROPERTY_DEFINITION_REPRESENTATION.DEFINITION')) \|

                       ('MATERIAL_PROPERTY_REPRESENTATION_SCHEMA.' +

                      'MATERIAL_PROPERTY_REPRESENTATION' IN

                      TYPEOF(temp)))) = 0);

END_ENTITY;

ENTITY product_material_composition_relationship

SUBTYPE OF (product_definition_relationship);

  class                : label;

  constituent_amount    : SET \[1:?\] OF characterized_product_composition_value;

  composition_basis    : label;

  determination_method : text;

END_ENTITY;

ENTITY property_definition_relationship;

  name                        : label;

  description                   : text;

  relating_property_definition  : property_definition;

  related_property_definition   : property_definition;

END_ENTITY;

END_SCHEMA;

## А.2 material_property_representation_schema

Настоящая схема является модифицированной версией одноименной схемы по ГОСТ Р ИСО 10303-45. Изменения включают удаление неиспользуемых в настоящем стандарте объектов и типов

SCHEMA material_property_representation_schema '{iso standard 10303 part(45) version(2) object(1) material_property_representation_schema(2)}';

REFERENCE FROM product_property_representation_schema

     (property_definition_representation);

     

REFERENCE FROM shape_dimension_schema

     (dimensional_characteristic_representation);

REFERENCE FROM process_property_representation_schema

     (action_property_representation,

      resource_property_representation);

REFERENCE FROM support_resource_schema

     (label,

      text);

TYPE characterized_property_representation = SELECT (

  action_property_representation,

  dimensional_characteristic_representation,

  property_definition_representation,

  resource_property_representation);

END_TYPE;

ENTITY data_environment;

  name          : label;

  description   : text;

  elements      : SET \[1:?\] OF characterized_property_representation;

END_ENTITY;

ENTITY data_environment_relationship;

  name                        : label;

  description               : text;

  relating_data_environment   : data_environment;

  related_data_environment    : data_environment;

END_ENTITY;

ENTITY material_property_representation

  SUBTYPE OF (property_definition_representation);

  dependent_environment : data_environment;

END_ENTITY;

ENTITY material_dimensional_characteristic_representation

  SUBTYPE OF (dimensional_characteristic_representation);

  dependent_environment : data_environment;

END_ENTITY;

END_SCHEMA;

## А.3 qualified_measure_schema

Настоящая схема является модифицированной версией одноименной схемы по ГОСТ Р ИСО 10303-45. Изменения включают удаление неиспользуемых в настоящем стандарте объектов и типов

SCHEMA qualified_measure_schema '{iso standard 10303 part(45) version(4) object(1) qualified_measure_schema(3)}';

REFERENCE FROM mathematical_functions_schema   -- ISO 10303-50

     (maths_value);

REFERENCE FROM measure_schema   -- ISO 10303-41

     (measure_with_unit,

unit);

REFERENCE FROM representation_schema   -- ISO 10303-43

     (representation_item);

REFERENCE FROM support_resource_schema   -- ISO 10303-41

     (identifier,

      label,

      text,

      bag_to_set);

TYPE value_format_type = identifier;

WHERE

      WR1: LENGTH(SELF) \<= 80;

END_TYPE; -- value_format_type

 

TYPE value_qualifier = SELECT

  (maths_value_precision_qualifier,

   precision_qualifier,

   type_qualifier,

   uncertainty_qualifier,

   value_format_type_qualifier);

END_TYPE;

ENTITY descriptive_representation_item

  SUBTYPE OF (representation_item);

  description : text;

END_ENTITY;

ENTITY expanded_uncertainty

  SUBTYPE OF (standard_uncertainty);

  coverage_factor : REAL;

END_ENTITY;

ENTITY maths_value_qualification;

  name      : label;

  description     : text;

  qualified_maths_value : maths_value_with_unit;

  qualifiers    : SET \[1:?\] OF value_qualifier;

WHERE

  WR1: SIZEOF(QUERY(temp \<\* qualifiers \|

             ('QUALIFIED_MEASURE_SCHEMA.PRECISION_QUALIFIER'

             IN TYPEOF(temp)) OR

       ('QUALIFIED_MEASURE_SCHEMA.MATHS_VALUE_PRECISION_QUALIFIER'

       IN TYPEOF(temp)))) \< 2;

  WR2: NOT ('REPRESENTATION_SCHEMA.REPRESENTATION_ITEM'

           IN TYPEOF(SELF\\maths_value_qualification.qualified_maths_value));

END_ENTITY;

ENTITY maths_value_representation_item

  SUBTYPE OF (representation_item, maths_value_with_unit);

END_ENTITY;

ENTITY measure_qualification;

  name      : label;

  description     : text;

  qualified_measure   : measure_with_unit;

  qualifiers    : SET \[1:?\] OF value_qualifier;

WHERE

  WR1: SIZEOF(QUERY(temp \<\* qualifiers \|

             ('QUALIFIED_MEASURE_SCHEMA.PRECISION_QUALIFIER'

             IN TYPEOF(temp)) OR

       ('QUALIFIED_MEASURE_SCHEMA.MATHS_VALUE_PRECISION_QUALIFIER'

       IN TYPEOF(temp)))) \< 2;

  WR2: NOT ('REPRESENTATION_SCHEMA.REPRESENTATION_ITEM'

           IN TYPEOF(SELF\\measure_qualification.qualified_measure));

END_ENTITY;

ENTITY measure_representation_item

  SUBTYPE OF (representation_item, measure_with_unit);

END_ENTITY;

ENTITY maths_value_precision_qualifier;

  precision_value : maths_value;

END_ENTITY;

ENTITY precision_qualifier;

  precision_value : INTEGER;

END_ENTITY;

ENTITY qualified_representation_item

  SUBTYPE OF (representation_item);

  qualifiers  : SET \[1:?\] OF value_qualifier;

WHERE

  WR1: SIZEOF(QUERY(temp \<\* qualifiers \|

             ('QUALIFIED_MEASURE_SCHEMA.PRECISION_QUALIFIER'

              IN TYPEOF(temp)) OR

             ('QUALIFIED_MEASURE_SCHEMA.MATHS_VALUE_PRECISION_QUALIFIER'

        IN TYPEOF(temp)))) \< 2;

END_ENTITY;

ENTITY qualitative_uncertainty

  SUBTYPE OF (uncertainty_qualifier);

  uncertainty_value : text;

END_ENTITY;

ENTITY standard_uncertainty

  SUPERTYPE OF (expanded_uncertainty)

  SUBTYPE OF (uncertainty_qualifier);

  uncertainty_value : REAL;

END_ENTITY;

ENTITY type_qualifier;

  name : label;

END_ENTITY;

ENTITY uncertainty_qualifier

 SUPERTYPE OF (ONEOF (standard_uncertainty,

                     qualitative_uncertainty));

  measure_name : label;

  description  : text;

END_ENTITY;

ENTITY value_format_type_qualifier;

  format_type : value_format_type;

END_ENTITY;

END_SCHEMA;

| УДК 006.1:006.354 ОКС 35.240.50                                                                                                    |
|------------------------------------------------------------------------------------------------------------------------------------|
| Ключевые слова: материал, информационная модель, схема данных, свойство материала, характеристика материала, обозначение материала |

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

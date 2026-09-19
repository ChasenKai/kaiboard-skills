# 社区素材库清单概览 / Community asset catalog

> 本文件是**检索用的清单概览**，帮 Agent 知道"有哪些源可用"。
> **本仓不分发任何 `.excalidrawlib` 实体文件** —— 素材是第三方作者的资产、各有其许可，
> 一律**按需从上游官方库获取**（见 `scripts/lib_resolver.py`）。

## 怎么用

```bash
python scripts/lib_resolver.py --search "<技术栈或图标名>"   # 跨源检索
python scripts/lib_resolver.py --ensure "<库名>"            # 取件并缓存到本地
```

取件后生成器会自动识别该库：Mode B 按图标名嵌入；Mode A 取元素数组后实时注入画布。

---

## 上游概览（excalidraw-libraries 自动生成）

# Excalidraw 素材库 Catalog 概览

> 数据源：`excalidraw/excalidraw-libraries` 官方 `libraries.json`（本文件为抓取时的快照概览；实时检索以 `lib_resolver.py` 拉取的索引为准）。

> 总库数 **231**，其中 **159** 个带组件级 `itemNames` 索引（可被 Agent 检索到单个图标）。


## 按主题分类

### 架构/系统设计（32 个）

- ArchiMate - Application Layer — Icons for Application Layer of ArchiMate - modeling language for Enterprise Architecture.  `18 组件`
- Architecture diagram components — Collection of common components for architecture diagrams.  `11 组件`
- Architecture floor plan symbols — Some furnitures an others symbols to help in architecture planning  `0 组件`
- Atlassian Product Suite — A comprehensive collection of logos for the Atlassian ecosystem. Includes Jira, Confluence  `7 组件`
- AWS Architecture Icons — A collection of AWS Icons  `4 组件`
- AWS Architecture Icons — AWS Architecture Icons  `249 组件`
- AWS Serverless Icons v2 — A new library with icons for AWS serverless services. This version has a new design and mo  `24 组件`
- Basic system design — System design templates  `7 组件`
- C4 Architecture — C4 Simon's Brown concept elements based on https://c4model.com/  `10 组件`
- Cloud — Collection of symbols related to cloud artefacts (logos of Kubernetes, Gardener, AWS, Azur  `0 组件`
- Cloud Design Patterns — A collection of cloud design patterns components (as defined in https://docs.microsoft.com  `0 组件`
- Databricks Architecture Icons — A collection of Databricks Icons  `24 组件`
- Google Icons — Icons for all Google Cloud Platform and Google Workspace products. The icons were extracte  `139 组件`
- Hexagonal Architecture — Useful to diagram and learn more about Hexagonal (aka Ports and Adapters) Architecture by   `0 组件`
- Information Architecture — A visual vocabulary for describing information architecture and interaction design, by Jes  `17 组件`
- IT icons — The shown icons are dedicated to the design of IT system architecture. The collection allo  `48 组件`
- Kubernetes icons — The full set of Kubernetes architecture icons, as published by @kubernauts on twitter on x  `74 组件`
- Kubernetes Icons Set — These icons are a way to standardize Kubernetes architecture diagrams for presentation. Ha  `19 组件`
- Microsoft Fabric Architecture Icons — Icons for Microsoft Fabric workloads, items, file types, and data sources. Not an official  `135 组件`
- Oracle Cloud Infrastructure Icons — A library of the common used icons for Oracle Cloud Infrastructure architecture draws like  `35 组件`
- Original Google Architecture Icons — Original Architecture icons for all Google Cloud Platform and Google Workspace products fr  `139 组件`
- Shapes for UML & ER Diagrams — An opinionated selection of shapes for UML & ER diagrams.  `0 组件`
- Software Architecture — Collection of software architecture components: microservice, database, cache, event bus o  `0 组件`
- Software Logos — Software architecture logos: archive, database, docker, JSON, Kubernetes, load balancer, P  `0 组件`
- System Design Components — Components useful in interviews and elsewhere to build high-level system diagrams.  `0 组件`
- System Design Icons — Generic components for use for a system design scenario  `3 组件`
- System Design Template — A standard structure and process for efficiently creating system designs with fill-in-the   `0 组件`
- UML Component Diagram — Different UML components used for making a component diagram. 

Component diagram shows co  `6 组件`
- UML Deployment diagram — Deployment diagram is a structure diagram which shows architecture of the system as deploy  `8 组件`
- UML Library: Activity Diagram — An excalidraw for any person interested in creating Activity Diagram in accordance with ru  `16 组件`
- Veeam — A collection of icons used for IT architecture design documents including Veeam backup com  `0 组件`
- VMware Architecture Design — Create awesome VMware architecture  `48 组件`

### 云厂商（13 个）

- AWS Serverless Icons — A collection of icons of AWS serverless services. This collection contains the icons of th  `0 组件`
- AWS Simple Icons — A collection of AWS Simple Icons with 3 different flavours (Monochrome, Colour and Colour   `0 组件`
- Azure cloud services icons — Collection of icons from different Azure cloud services.  `19 组件`
- Azure Compute — All the most common Azure compute icons from the Azure portal  `17 组件`
- Azure Containers — Collection of the most common Azure Container icons from the Azure portal.  `6 组件`
- Azure General — All the Azure General items from the Azure Portal  `19 组件`
- Azure Network — All of the most common Azure network icons from the Azure portal  `29 组件`
- Azure Storage — Most common Azure storage icons from the Azure portal  `13 组件`
- GCP Icons — Google Cloud Platform product icons.  `0 组件`
- Microsoft Azure cloud icons — Microsoft unofficial Azure icon line drawings  `19 组件`
- Misc Azure Icons — Some more Azure Icons that I have not found in other libraries  `7 组件`
- Some more logos — Android, Windows, Linux, Kong, Let's Encrypt, Keycloak, Salesforce and Azure logo  `8 组件`
- Technology Logos — Collection of technology logos mostly from the cloud-native space. Featuring: Kubernetes,   `0 组件`

### 容器/编排/K8s（1 个）

- Dev Ops Icons — A collection of icons for Dev Ops work, including the hashistack: Nomad, Consul, Vault and  `0 组件`

### 数据/数据库（6 个）

- Data sources — Data sources, protocols, apis, and sinks - USB, email, FTP, kafka, GraphQL, databases, RES  `6 组件`
- Database — A collection of icons and graphics for drawing database infrastructures in the cloud and o  `0 组件`
- Flow Chart Symbols — Common symbols used in flow chart, including: Start / End, Process, Decision, Document, Mu  `15 组件`
- IT Logos — Some IT logos: MySQL, PHP, Jenkins, Tomcat, Bower, npm, Red Hat  `7 组件`
- Kafka Streams Topology Design — Kafka Streams Topology Design is an open standard dedicated to the clear and effective des  `72 组件`
- Redis Grafana — A collection of Redis and Grafana related icons: Redis, Redis Enterprise, Grafana, Prometh  `0 组件`

### 网络/安全（6 个）

- Common Home Network Basics — Common items found in a Home Lab / Network: Network Switch, File Folder, Server, Security   `8 组件`
- CyberArk — Iconography related to CyberArk's Identity Security Platform, applications, components, se  `52 组件`
- Fibre Network — Useful Fibre Network Assets  `3 组件`
- Network elements — Several common network element icons.  `5 组件`
- Network locations — Locations for network macro designs. This library allows for representing main corporate o  `5 组件`
- Network topology icons — Several of the most common network topology icons.  `10 组件`

### DevOps/CI（3 个）

-  GitHub Actions — This library provides a set of essential items to streamline your GitHub Actions workflows  `4 组件`
- Excalidraw Archimate Template — This is a collection of Excalidraw objects, covering the business, application, and techno  `38 组件`
- GitHub Git Icons — Basic GitHub Icons for educational purposes. The icons include git branch, git commit, com  `0 组件`

### IT 图标/Logo（15 个）

- Camunda Platform Icons — Icons for the Camunda Platform stack and Camunda in general.



This library includes: Cam  `12 组件`
- Data Science logos — A collection of data science tool icons. Inlcuding: Airflow, Jupyter, Pandas, Numpy, Tenso  `0 组件`
- Elixir — Some logos from the elixir/erlang family  `6 组件`
- FAIR web icons — Icons and software logos for everything related to the semantic web and the FAIR principle  `4 组件`
- Front End Tools & Technologies — A collection of logos related to front end technologies, tools and sites.  `0 组件`
- HashiCorp — A collection of HashiCorp product logos.  `8 组件`
- HTML, CSS and JS logos — A collection of core web development technology logos  `0 组件`
- Internet Service providers — Logos of internet service providers  `7 组件`
- IT Logos — A collection of IT logos, including languages, frameworks and tools for building web appli  `31 组件`
- IT Tools Logos — This library contains logos from tools of different purposes that are still missing in Exc  `5 组件`
- Microsoft 365 icons — Excalidraw replicas of common Microsoft 365, Microsoft Viva and related logos.



Not an o  `37 组件`
- Nextflow - Seqera - nf-core — Logos for Seqera and it's products (Nextflow, MultiQC, Wave, Fusion).

Logo for nf-core, a  `14 组件`
- PRINTERS — There's some printers icon I worked on.

It's gonna be full of type of printers and brand   `3 组件`
- Random figure drawings — Random figure drawings for logos and much more.  `0 组件`
- TomorrowX Composable Agentic Platform (CAP) — TomorrowX Composable Agentic Platform (CAP) icon set  `4 组件`

### 流程图/判定（8 个）

- bpmn — icon of bpmn diagram  `34 组件`
- Data Flow — For Data Flow diagrams  `4 组件`
- Data processing — Items to visualize steps during data processing.  `8 组件`
- Decision flow control — Yes/no condition boxes for diagramming.  `0 组件`
- Digital Signal Processing — A set of operation blocks for digital signal processing  `8 组件`
- Medias — Collection of components related to media: coverflow, video player, playback controls, vol  `0 组件`
- Piping and instrumentation diagram P&ID — Basic symbols to quickly sketch a piping and instrumentation diagram.

Used in chemical pr  `28 组件`
- Wardley Mapping Canvas — The Wardley Mapping Canvas helps newcomers with their first mapping experiences by offerin  `12 组件`

### UI/线框/原型（32 个）

- Android — Collection of Android components.  `0 组件`
- Arduino Boards — A collection of five Arduino boards: Uno, Uno-clone, Nano, Leonardo, and Mega. The drawing  `0 组件`
- Arduino Micro — Arduino Micro board  `0 组件`
- Body Builder Kit 1 — Various elements to build bodies with unique characteristics. Includes several variations   `15 组件`
- Character Kit 1 — A collection of characters built with "Body Builder Kit 1" and "Head Builder Kit 1". Uses   `2 组件`
- Circuit Components — A collection of circuit components for easy circuit diagramming.  `24 组件`
- Desktop Resolutions — Blank desktop frames of common resolutions. Use to wireframe desktop apps.  `0 组件`
- DnD/TTRPG battle map creature tokens — A bunch of tokens you can use on a DnD battle map. Different colours and numbers make them  `1 组件`
- DomainStoryTelling — https://domainstorytelling.org/quick-start-guide  `7 组件`
- ecommerce mobile ui — Webkul creates with love for the community, enabling quick wireframe creation for upcoming  `75 组件`
- Electrical Engineering — Contains the most common components to develop one-line diagrams for AC Systems. More to c  `15 组件`
- Event Storming — Includes the common components for an event storming session. 



The colors are slightly   `7 组件`
- Forms — Collection of form components.  `0 组件`
- Head Builder Kit 1 — Various elements to build heads with unique characteristics. Includes several variations a  `49 组件`
- HTML input elements — Basic HTML input elements for app wireframes. Elements include types: button, number, date  `8 组件`
- Lo-Fi Wireframing Kit — A collection of Lo-Fi wireframing components.  `0 组件`
- Maps — Basic map components in style of Google Maps. One with location pins and set of location p  `0 组件`
- Message Queue components — Components for Message Queue diagrams (such as for IBM MQ)  `6 组件`
- NSX-T VMware — A collection of icons used for design documents including NSX-T VMware components. RunNSX  `0 组件`
- Organic Chemistry Basics — Basic building blocks for creating organic molecules. Note that there is a white circle be  `27 组件`
- Playing cards — French-suited playing card aces  `5 组件`
- Racks and Servers / Components — Quick diagrams for datacenter layout and server / component documentation  `5 组件`
- Raspberry Pi 3 — A Raspberry Pi 3 header component.  `0 组件`
- Raspberry Pi Zero — A Raspberry Pi Zero header component.  `0 组件`
- Risk based Test Strategy — Components to run Risk-based Test Strategy planning session.  `8 组件`
- Systems Design Components — Simple library to help with Systems Design  `6 组件`
- Thicc arrow — Arrow shape that can be modified in a number of ways to suit different use cases. This is   `3 组件`
- Universal UI kit — Universal UI, UX kit for app or web  `22 组件`
- Wardley Maps Symbols — A collection of Wardley Maps components and symbols. It contains symbols for: the Componen  `0 组件`
- Web Kit — A collection of commonly used web components.  `0 组件`
- Webpage frames — These components can be used while creating design for web pages to explain the concepts l  `3 组件`
- Wireframing placeholders — Content placeholders for wireframe diagrams  `10 组件`

### 图示/白板元素（15 个）

- 3D Shapes — A couple of 3D shapes  `2 组件`
- Basic shapes — Basic shapes for simple drawings.  `0 组件`
- DnD 5e planning — Icons to use for campaign planning. Plan ability checks, rests, notes and more.   `42 组件`
- Domain-Driven Design — Default sticky convention for event storming exercises  `16 组件`
- ELK Stack — The icons to handle ELK technologies.  `5 组件`
- Mathematical Symbols — Commonly-used symbols in mathematics. Symbols are designed to look good next to text in th  `15 组件`
- Montessori Basic Grammar Symbols — For use in teaching parts of speech using the Montessori basic grammar symbols. Sized for   `10 组件`
- Music Instruments — collection of instruments like keyboard, drums, flute, clapbox, Musical notes, Radio and S  `0 组件`
- Schematic Symbols — A collection of common electrical schematic wiring diagram symbols. The drawings are sized  `0 组件`
- Simple Sticky Notes — Simplistic sticky notes based on Rectangles and inner texts. The benefit is that the text   `7 组件`
- some-handdrawn-signs — Some useful handdrawn signs, ugly and imperfect as they should be.  `2 组件`
- Stick people — Simple Stick people. You can change postures by deep-select  and changing the arms (elbows  `7 组件`
- Sticky Notes — Post its in every color for your design thinking sessions.  `0 组件`
- Team Topologies — Collection of shapes to describe your organization's Team Topology (as defined by https://  `0 组件`
- Veeam unofficial — A collection of unofficial icons inspired from the Veeam Visio shapes we all know and like  `0 组件`

### 人物/角色（2 个）

- Baby Characters — Drawings of famous baby characters.
The drawings were based on Pinterest and howtodrawfork  `4 组件`
- Simple Characters — Library of simple characters  `49 组件`

### 图标记号/箭头（21 个）

- Artem's icons — Icons for concept boards  `22 组件`
- Astronomical Symbols — A library of astronomical symbols for the sun, the moon, the earth, planets and the zodiac  `27 组件`
- Awesome Icons — A growing collection of do whatever you want icons.  `0 组件`
- Clouds — Cloud icons for topic holders in mind maps  `4 组件`
- Comms Platform Icons — Icons of various comms platforms  `6 组件`
- Dart and Flutter icons — Dart and Flutter icons to use for your drawings on excalidraw !

  `2 组件`
- Data Platform — Icon of Data Stack, following realistic + simplicity style. To be updated continously. Let  `33 组件`
- Enterprise Integration Patterns — Mostly complete representation of the icons from the excellent Enterprise Integration Patt  `42 组件`
- Football Icons — Icons representing some of the common football symbols.  `6 组件`
- Go Icons — Collection of icons related to the Go programming language.  `2 组件`
- Halloween — Elements (stickers) for Halloween-themed designs.  `39 组件`
- Icons — an icon library  `65 组件`
- Microsoft Apps — A collection of icons for Microsoft's Power Platform and Office 365 apps.  `8 组件`
- Music notation — Symbols for writing music in the staff and for writing rhythms. 

Can be used for self-stu  `23 组件`
- R Icons — R and RStudio icons.  `0 组件`
- Red Hat — Red Hat product icons  `3 组件`
- Snowflake datawarehousing Icons — Collection of Snowflake datawarehouse icons.  `0 组件`
- Snowflake Iconography — An exhaustive list of Snowflake DB icons  `54 组件`
- System Icons — Some system icons  `24 组件`
- Traffic signs ⛔🛑 — Traffic signs are commonly known and help you symbolize many ideas easily.  `9 组件`
- Web3 Crypto Solution Design v1 — Symbols for solution design of web3 applications like NFT collections or DAO. Future versi  `10 组件`

### 地图/地理（1 个）

- Customer Journey Map — For creating your own Customer Journey Map, it has small and big templates.  `0 组件`

### 业务/通用（5 个）

- Business Model Templates — A collection of templates for canvases that can be used to model various business aspects.  `0 组件`
- Gantt Diagram — A Gantt diagram template you can use to plan your projects.  `0 组件`
- Make your calendar — There is a template for every month. For making clender of an year all you have to do, for  `8 组件`
- Organization Chart — Org chart template  `9 组件`
- Scrum board — Scrum board for agile development  `0 组件`


## 高频候选（架构 / 系统设计类常用，可优先取件）

-  GitHub Actions — `devdaejungyoon/github-actions.excalidrawlib` — 4 组件
- 3d coordinate systems + graphs — `aimpizza/3d-coordinate-systems-graphs.excalidrawlib` — 5 组件
- ArchiMate - Application Layer — `dmtwng/archimate-application-layer.excalidrawlib` — 18 组件
- Architecture diagram components — `anna-pastushko/architecture-diagram-components.excalidrawlib` — 11 组件
- Architecture floor plan symbols — `Arqtangeles/architecture.excalidrawlib` — 0 组件
- Arduino Boards — `rkjc/arduino-boards.excalidrawlib` — 0 组件
- Arduino Micro — `jasoncoelho/arduino-micro.excalidrawlib` — 0 组件
- Artem's icons — `artem-anufrij-live-de/artem-s-icons.excalidrawlib` — 22 组件
- Atlassian Product Suite — `jatinkrmalik/atlassian-product-suite.excalidrawlib` — 7 组件
- Awesome Icons — `ferminrp/awesome-icons.excalidrawlib` — 0 组件
- AWS Architecture Icons — `narhari-motivaras/aws-architecture-icons.excalidrawlib` — 4 组件
- AWS Architecture Icons — `childishgirl/aws-architecture-icons.excalidrawlib` — 249 组件
- AWS Serverless Icons — `slobodan/aws-serverless.excalidrawlib` — 0 组件
- AWS Serverless Icons v2 — `stojanovic/aws-serverless-icons-v2.excalidrawlib` — 24 组件
- AWS Simple Icons — `husainkhambaty/aws-simple-icons.excalidrawlib` — 0 组件
- Azure cloud services icons — `youritjang/azure-cloud-services.excalidrawlib` — 19 组件
- Azure Compute — `7demonsrising/azure-compute.excalidrawlib` — 17 组件
- Azure Containers — `7demonsrising/azure-containers.excalidrawlib` — 6 组件
- Azure General — `7demonsrising/azure-general.excalidrawlib` — 19 组件
- Azure Network — `7demonsrising/azure-network.excalidrawlib` — 29 组件
- Azure Storage — `7demonsrising/azure-storage.excalidrawlib` — 13 组件
- Baby Characters — `claracavalcante/baby-characters.excalidrawlib` — 4 组件
- Banners — `sketchingdev/banners.excalidrawlib` — 7 组件
- Barotrauma — `danielpza/barotrauma.excalidrawlib` — 27 组件
- Basic system design — `pratheeshpm/basic-system-design.excalidrawlib` — 7 组件
- Basic UX/wireframing elements — `gabrielamacakova/basic-ux-wireframing-elements.excalidrawlib` — 69 组件
- Boardgame — `pocomane/boardgame.excalidrawlib` — 10 组件
- Body Builder Kit 1 — `pixelass/body-builder-kit-1.excalidrawlib` — 15 组件
- bpmn — `fraoustin/bpmn.excalidrawlib` — 34 组件
- Bullet Journal Trackers — `booknerdonmars/bullet-journal-trackers.excalidrawlib` — 2 组件
- C4 Architecture — `dmitry-burnyshev/c4-architecture.excalidrawlib` — 10 组件
- Camunda Platform Icons — `itsmestefanjay/camunda-platform-icons.excalidrawlib` — 12 组件
- Character Kit 1 — `pixelass/character-kit-1.excalidrawlib` — 2 组件
- Chickens — `kvmet/chickens.excalidrawlib` — 3 组件
- Circuit Components — `mppowell/circuit-components.excalidrawlib` — 24 组件
- Cloud — `cloud/cloud.excalidrawlib` — 0 组件
- Cloud Design Patterns — `michelcaradec/cloud-design-patterns.excalidrawlib` — 0 组件
- Clouds — `dimitrios-fkliaras/clouds.excalidrawlib` — 4 组件
- Collective operation — `https-github-com-jinmingyi1998/collective-operation.excalidrawlib` — 8 组件
- Common Home Network Basics — `dday987/common-home-network-basics.excalidrawlib` — 8 组件
- Comms Platform Icons — `adamkdean/comms-platform-icons.excalidrawlib` — 6 组件
- Computer parts — `rochacbruno/computer-parts.excalidrawlib` — 8 组件
- Computers — `ei-au/computers.excalidrawlib` — 0 组件
- Cryptocurrencies — `newbyca/cryptocurrencies.excalidrawlib` — 0 组件
- Customer Journey Map — `braweria/customer-journey-map.excalidrawlib` — 0 组件
- CyberArk — `infamousjoeg/cyberark.excalidrawlib` — 52 组件
- Dart and Flutter icons — `david-prta/dart-and-flutter-icons.excalidrawlib` — 2 组件
- Data Flow — `wmartzh/data-flow.excalidrawlib` — 4 组件
- Data Platform — `chuqbach/data-platform.excalidrawlib` — 33 组件
- Data Science logos — `farisology/data-science.excalidrawlib` — 0 组件

## 架构强相关库 · 组件抽样（search 检索粒度示例）

### IT Logos

- source: `pclainchard/it-logos.excalidrawlib`
- 组件 e.g.: Angular v2, Angular v1, Argo CD, BonitaSoft, Docker, Excalidraw v1, Excalidraw v2, Firebase, Flux CD, GitLab, Kafka, Kanoma

### Azure cloud services icons

- source: `youritjang/azure-cloud-services.excalidrawlib`
- 组件 e.g.: Key Vault, Application Insights, Azure DevOps, Network Interface, Public IP Address, Disk, Azure logo, Subscription, Resource Group, Blob Storage, Network Security Group, Virtual Network

### System Design Icons

- source: `niknm/systemdesignicons.excalidrawlib`
- 组件 e.g.: MapReduce, ServiceCluster, cacheLayer

### Baby Characters

- source: `claracavalcante/baby-characters.excalidrawlib`
- 组件 e.g.: Baby Yoda - No Colors, Baby Yoda - With Color, Baby Groot - No Colors, Baby Groot - With Color

### AWS Architecture Icons

- source: `narhari-motivaras/aws-architecture-icons.excalidrawlib`
- 组件 e.g.: Lambda, ELB, EC2, Lambda

### Network topology icons

- source: `dwelle/network-topology-icons.excalidrawlib`
- 组件 e.g.: Computer w/ keyboard (3D), Computer w/ keyboard and mouse (3D), Computer (3D), VPN, Firewall, Server, Switch, Hub, Router, Client

### Math Teacher Library

- source: `https-github-com-ytrkptl/math-teacher-library.excalidrawlib`
- 组件 e.g.: Dotted Coordinate Grid With Axes Labeled, Basic Venn Diagram, Coordinate Grid With Axes Labeled, Number Line with Labels, Blank Number Line, Sphere Diagram Colored, Sphere Diagram, Rectangular Prism Cube, Rectangular Prism Cuboid, Parallel Lines and Transversal With Symbol, Parallel Lines and Transversal Without Symbol, Blank Graph Paper Coordinate Grid

### IT Logos

- source: `selanas/it-logos.excalidrawlib`
- 组件 e.g.: MySQL, PHP, Jenkins, Tomcat, Bower, npm, Red Hat

### Wireframing placeholders

- source: `xxxdeveloper/wireframing-placeholders.excalidrawlib`
- 组件 e.g.: Blue Widget, Red Widget,  Yellow Widget, Green Widget, Overall structure diagram, Blue Widget (light), Red Widget (light), Overall structure diagram (light),  Yellow Widget (light), Green Widget (light)

### Network elements

- source: `samu_x86/network-elements.excalidrawlib`
- 组件 e.g.: Switch, Edge, Load Balancer, Firewall, Router

### Electrical Engineering

- source: `risjain/electrical-engineering.excalidrawlib`
- 组件 e.g.: PV panel, Transformer One-line, DQ0 to ABC Conversion, ABC to DQ0 Conversion, Transformer with Core, Bus Bar, Inductor, Circuit Breaker, Potential Transformer, Current Transformer, Resistor, Ground

### Retail peripherals

- source: `esteevens/retail-peripherals.excalidrawlib`
- 组件 e.g.: Payment terminal, Barcode scanner, Receipt printer

### Fibre Network

- source: `fibreninja/fibre-network.excalidrawlib`
- 组件 e.g.: C6, B6, FIST

### Computer parts

- source: `rochacbruno/computer-parts.excalidrawlib`
- 组件 e.g.: mouse, hard disk, chip, cpu, headphones, keyboard, display, ram

### Racks and Servers / Components

- source: `jgodoy/racks-and-servers-components.excalidrawlib`
- 组件 e.g.: 8U Rack, 16U Rack, 4U Server, 2U Server / Component, 1U Server / Component

### Azure Network

- source: `7demonsrising/azure-network.excalidrawlib`
- 组件 e.g.: Virtual Gateways, Local Gateways, Connections, Firewalls, Firewall Policies, Firewall Manager, IP Groups, NAT Gateways, App Gateways, Traffic Manager Profiles, DNS ZOnes, Bastions

### Azure Containers

- source: `7demonsrising/azure-containers.excalidrawlib`
- 组件 e.g.: Container Registires, Batch Accounts, Service Fabric Clusters, App Services, Container Instances, Kubernetes Services

### Azure General

- source: `7demonsrising/azure-general.excalidrawlib`
- 组件 e.g.: Azure, Preview Features, Resource Explorer , Reservations, Free Services, Share Dashboards, Quickstart, What's New, Tags, Templates, Service Health, Help and Support

### Dart and Flutter icons

- source: `david-prta/dart-and-flutter-icons.excalidrawlib`
- 组件 e.g.: Dart, Flutter

### Network locations

- source: `jgodoy/network-locations.excalidrawlib`
- 组件 e.g.: Corporate Office / Headquarterts, Office, City, House, Datacenter

### Internet Service providers

- source: `tuckdiaz/internet-service-providers.excalidrawlib`
- 组件 e.g.: BT, Airtel, Singtel, Verizon, At&t, T-Mobile , TataCommunications

### Banners

- source: `sketchingdev/banners.excalidrawlib`
- 组件 e.g.: Messy Banner, Large Bookmark, Right Side Banner, Arrow Banner, Double Banner, Stylised Banner, Classic Banner

### C4 Architecture

- source: `dmitry-burnyshev/c4-architecture.excalidrawlib`
- 组件 e.g.: C4 elements, Person, Web App, Mobile App, Component, System, Existing System, Database, Group, Relation

### PRINTERS

- source: `krustvalentin/printers.excalidrawlib`
- 组件 e.g.: BIG Printer, SMOL Printer, HP

### UML Library: Activity Diagram

- source: `https-github-com-papacrispy/uml-library-activity-diagram.excalidrawlib`
- 组件 e.g.: Initial State, Final State, Terminate, Action Box, Item Box, Decision Box_1, Decision Box_2, Fork/ Join Node, Expansion Region Entry/Exit Point, Expansion Description_Iterative, Expansion Description_Parallel, Expansion Description_Stream

### Common Home Network Basics

- source: `dday987/common-home-network-basics.excalidrawlib`
- 组件 e.g.: Wireless Router, Security Camera, Network Switch, File Folder, Server, Access Point, Cloud, Wifi Symbol

### Enterprise Integration Patterns

- source: `stuc2010/enterprise-integration-patterns.excalidrawlib`
- 组件 e.g.: Dead letter channel, Channel adapter L, Channel adapter R, Message filter, Test data generator, Test data verifier, Channel purger, Message dispatcher, Content filter, Unwrapper, Smart proxy, Wire tap

### Body Builder Kit 1

- source: `pixelass/body-builder-kit-1.excalidrawlib`
- 组件 e.g.: Example 1, Example 2, Example 3, Example 4, Contour Female 1, Body Female 1, Body Male 1, Contour Male 1, Pants 1, Pants 2, Pants 3, Pants 4

### Character Kit 1

- source: `pixelass/character-kit-1.excalidrawlib`
- 组件 e.g.: Spiderman, Zombie

### Female Heads Diverse

- source: `pixelass/female-heads-diverse.excalidrawlib`
- 组件 e.g.: Female Alien, Female Zombie, Female African, Female European, Female Latino, Female Indian, Female Asian, Female Elderly

### Head Builder Kit 1

- source: `pixelass/head-builder-kit-1.excalidrawlib`
- 组件 e.g.: Hair 8, Hair 9, Example 1, Example 2, Beard 9, Beard 7, Hat 3, Hat 2, Hat 1, Beard 10, Head 2, Nose 1

### Male Heads Diverse 1

- source: `pixelass/male-heads-diverse-1.excalidrawlib`
- 组件 e.g.: Male 1, Male Magician 1, Male Musician 1, Male Soldier 1, Male Trucker 1, Male Alien, Male Gangster 1, Abraham Lincoln 1, Male Elderly 1, Male 2, Male Punk 1, Male Zombie 1

### Golang gophers

- source: `gregory/golang-gophers.excalidrawlib`
- 组件 e.g.: gopher front, gopher up, gopher right, gopher angle, gopher left, gopher down

### Universal UI kit

- source: `manuelernestog/universal-ui-kit.excalidrawlib`
- 组件 e.g.: Tooltip, Circle Progress Bar, User Icon, Toggle Unchecked, Pie chart, Line chart, Bar Chart, Calendar, Search Input, Slider, Alert, Horizontal Scroll 

### Kubernetes Icons Set

- source: `lowess/kubernetes-icons-set.excalidrawlib`
- 组件 e.g.: rolebinding, user, serviceaccount, volume, pv, pvc, namespace, job, cronjob, crd, clusterrolebinding, secret

### Kubernetes icons

- source: `boemska-nik/kubernetes-icons.excalidrawlib`
- 组件 e.g.: ns, ns-text, pod, pod-text, rs, rs-text, deploy, deploy-text, ds, ds-text, sts, sts-text

### AWS Serverless Icons v2

- source: `stojanovic/aws-serverless-icons-v2.excalidrawlib`
- 组件 e.g.: Lambda, AppSync, APIGateway, DynamoDB, Aurora, EventBridge, SQS, SNS, S3, CloudFront, SES, CloudWatch

### ecommerce mobile ui

- source: `webkul/ecommerce-mobile-ui.excalidrawlib`
- 组件 e.g.: category page, checkout page, cart page, product page, homepage, product image, gallery-6, gallery-4, gallery-3-a, gallery-3-b, banner, carousel banner

### Basic system design

- source: `pratheeshpm/basic-system-design.excalidrawlib`
- 组件 e.g.: MediaService, NotificationService, APIGateway, Analytics, Database, SearchService, LBWithDbNRepicas

### Bullet Journal Trackers

- source: `booknerdonmars/bullet-journal-trackers.excalidrawlib`
- 组件 e.g.: Year In Pixels (Mood Tracker), Habit Tracker

### Simple Characters

- source: `moochin/simple-characters.excalidrawlib`
- 组件 e.g.: Stockholm Syndrome, Rollercoaster, Confused, Game, Time travel, Broken Tower, Tower, Toolbox, Sugar rush, Sweets, Evil Plan, Hostage

### Nextflow - Seqera - nf-core

- source: `ewels/nextflow-seqera-nf-core.excalidrawlib`
- 组件 e.g.: Stations - 3, Stations - 2, VCF - multiple, BAM - multiple, FastQ - multiple, VCF file, BAM file, FastQ file, nf-core logo, Fusion logo, Wave logo, Seqera logo

### AWS Architecture Icons

- source: `childishgirl/aws-architecture-icons.excalidrawlib`
- 组件 e.g.: CloudSearch, EMR, Lake Formation, Data Lake, Kinesis, Kinesis Video Streams, Kinesis Data Streams, Kinesis Data Firehose, Kinesis Data Analytics, Managed Service for Apache Flink, Glue, Crawler

### Collective operation

- source: `https-github-com-jinmingyi1998/collective-operation.excalidrawlib`
- 组件 e.g.: reduce scatter, all to all, all gather, all reduce, gather, reduce, broadcast, scatter

### ArchiMate - Application Layer

- source: `dmtwng/archimate-application-layer.excalidrawlib`
- 组件 e.g.: Application Component, Application Component Icon, Application Collaboration, Application Collaboration Icon, Application Interface, Application Interface Icon, Application Function, Application Function Icon, Application Interaction, Application Interaction Icon, Application Process, Application Process Icon

### UML Deployment diagram

- source: `jordangeurtsen/uml-deployment-diagram.excalidrawlib`
- 组件 e.g.: Deployment pane, Scheme icon, Artifact icon, Scheme icon, Artifact icon, Operating system, Execution environment, Exposed interface

### UML Component Diagram

- source: `jordangeurtsen/uml-component-diagram.excalidrawlib`
- 组件 e.g.: Dependency, Port, Provided interface, Required interface, Subsystem, Component

### CyberArk

- source: `infamousjoeg/cyberark.excalidrawlib`
- 组件 e.g.: app-window, cloud-vault, x, checkmark, web-app, laptop, clock, document, secret-key, key, psm-recording, horizontal-nlb

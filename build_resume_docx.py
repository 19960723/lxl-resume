from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


OUT = "林小龙-全栈开发工程师简历-母版.docx"

FONT_CN = "微软雅黑"
FONT_EN = "Arial"
COLOR_INK = RGBColor(31, 41, 55)
COLOR_MUTED = RGBColor(91, 101, 117)
COLOR_ACCENT = RGBColor(29, 78, 216)
COLOR_LINE = "D7DEE8"


def set_run_font(run, size=None, bold=None, color=None):
    run.font.name = FONT_EN
    run._element.rPr.rFonts.set(qn("w:ascii"), FONT_EN)
    run._element.rPr.rFonts.set(qn("w:hAnsi"), FONT_EN)
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if color is not None:
        run.font.color.rgb = color


def set_paragraph_border_bottom(paragraph, color=COLOR_LINE, size="8", space="6"):
    p = paragraph._p
    p_pr = p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), size)
    bottom.set(qn("w:space"), space)
    bottom.set(qn("w:color"), color)
    p_bdr.append(bottom)


def add_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(text)
    set_run_font(run, 12, True, COLOR_ACCENT)
    set_paragraph_border_bottom(p, size="6", space="4")
    return p


def add_body(doc, text="", size=9.5, bold=False, color=COLOR_INK, after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.08
    run = p.add_run(text)
    set_run_font(run, size, bold, color)
    return p


def add_kv_line(doc, label, value):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    label_run = p.add_run(label)
    set_run_font(label_run, 9.5, True, COLOR_INK)
    value_run = p.add_run(value)
    set_run_font(value_run, 9.5, False, COLOR_INK)
    return p


def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Cm(0.45 + level * 0.3)
    p.paragraph_format.first_line_indent = Cm(-0.22)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(text)
    set_run_font(run, 9.2, False, COLOR_INK)
    return p


def add_role(doc, date, title, org):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    r1 = p.add_run(date)
    set_run_font(r1, 9.5, True, COLOR_INK)
    r2 = p.add_run("  |  ")
    set_run_font(r2, 9.5, False, COLOR_MUTED)
    r3 = p.add_run(title)
    set_run_font(r3, 9.5, True, COLOR_INK)
    r4 = p.add_run("  |  ")
    set_run_font(r4, 9.5, False, COLOR_MUTED)
    r5 = p.add_run(org)
    set_run_font(r5, 9.5, False, COLOR_INK)


def add_project(doc, date, name, stack, intro, bullets):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)
    r1 = p.add_run(f"{date}  {name}")
    set_run_font(r1, 10, True, COLOR_INK)
    p2 = add_body(doc, intro, size=9.2, after=1.5)
    p2.paragraph_format.line_spacing = 1.05
    add_kv_line(doc, "技术栈：", stack)
    for item in bullets:
        add_bullet(doc, item)


def configure_document(doc):
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.25)
    section.bottom_margin = Cm(1.25)
    section.left_margin = Cm(1.35)
    section.right_margin = Cm(1.35)
    section.header_distance = Cm(0.8)
    section.footer_distance = Cm(0.8)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = FONT_EN
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = COLOR_INK

    for style_name in ["List Bullet", "List Paragraph"]:
        style = styles[style_name]
        style.font.name = FONT_EN
        style._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
        style.font.size = Pt(9.2)


def build():
    doc = Document()
    configure_document(doc)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(2)
    run = title.add_run("林小龙")
    set_run_font(run, 20, True, COLOR_INK)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.paragraph_format.space_after = Pt(5)
    r = subtitle.add_run("全栈开发工程师 / 前端开发工程师")
    set_run_font(r, 10.5, False, COLOR_MUTED)

    contact = doc.add_paragraph()
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.paragraph_format.space_after = Pt(7)
    r = contact.add_run("18岁[待确认]  |  湖南省娄底市  |  13290731298  |  1847426505@qq.com")
    set_run_font(r, 9.3, False, COLOR_MUTED)

    add_heading(doc, "个人优势")
    for item in [
        "7年以上 Web 应用开发经验，具备前端工程化、Node 服务开发、容器化部署和运维协作的复合型交付能力。",
        "前端侧长期负责 PC 客户端、后台管理、H5 嵌入页、可视化平台等多端业务；服务端侧可参与接口设计、业务服务开发和前后端联调。",
        "具备 Vue、React、Electron、TypeScript、Node.js 等技术实践经验，能独立推进模块设计、组件封装、服务集成和项目规范落地。",
        "有 IM 通讯、TRTC/WebRTC 音视频、多窗口桌面端交互、文件同步、本地缓存、地图/大屏可视化等复杂业务经验。",
        "具备 Node 服务开发、Docker 容器化部署、Kubernetes 运维协作相关经验，可参与从前端开发到服务部署的完整交付链路。",
    ]:
        add_bullet(doc, item)

    add_heading(doc, "专业技能")
    add_bullet(doc, "前端开发：HTML5、CSS3、Sass/Less、JavaScript、ES6、TypeScript、Canvas；熟悉 Vue、React、Element UI、vue-element-admin。")
    add_bullet(doc, "客户端与多端：Electron、uni-app、小程序、H5 嵌入页；有 PC 客户端、多窗口桌面端和移动端适配经验。")
    add_bullet(doc, "服务端开发：Node.js、Express、Koa2；可参与接口设计、业务服务开发、权限后台、业务中台和前后端联调。")
    add_bullet(doc, "工程化与协作：Vite、Webpack、Gulp、ESLint、Prettier、Mock、Git、SVN；熟悉项目规范、模块封装和构建优化。")
    add_bullet(doc, "部署与运维：Docker 镜像构建、容器编排部署、Kubernetes 基础运维协作；了解服务发布、环境配置、日志查看和问题排查流程。")
    add_bullet(doc, "业务集成：音视频 SDK、TRTC/WebRTC、地图 API、ECharts 可视化、IM 通讯、文件同步等复杂业务接入。")

    add_heading(doc, "工作经历")
    add_role(doc, "2021.06 - 至今", "Web 前端高级工程师", "公司名称待确认")
    add_bullet(doc, "负责核心项目的前端开发、项目成员协作、复杂功能方案设计、难点攻关、项目规范建设和功能迭代。")

    add_role(doc, "2021.04 - 2022.06 [时间待确认]", "Web 前端工程师", "公司名称待确认")
    add_bullet(doc, "参与公司内部 PC 客户端办公应用、后台管理系统、H5 嵌入原生移动端页面等业务开发。")
    add_bullet(doc, "推进前端项目代码规范、项目结构优化、版本迭代和相关文档沉淀。")

    add_role(doc, "2018.08 - 2021.01", "Web 前端工程师", "公司名称待确认")
    add_bullet(doc, "负责前端项目开发与维护，覆盖公司官网、小程序、后台管理、可视化调度平台等方向。")
    add_bullet(doc, "参与屏幕播控相关系统的重构、功能扩展和项目交付。")

    add_role(doc, "2018.01 - 2018.06", "Web 前端实习生", "公司名称待确认")
    add_bullet(doc, "参与前端页面制作、功能交互实现、问题修复和数据接口文档编写。")

    add_heading(doc, "项目经历")
    add_project(
        doc,
        "2022.06 - 至今",
        "协同/音视频类系统 [项目名待确认]",
        "Vue / Electron / Element UI / Axios / Mock / ESLint / Prettier / TRTC / jeecgboot",
        "项目包含客户端与后台管理两部分，覆盖多窗口桌面端交互、IM 通讯、腾讯 TRTC 音视频会议、文件同步、人员/招聘/薪资/权限等后台模块。",
        [
            "负责 Electron 客户端核心模块开发，包括多窗口通信、事件分发、窗口透明、节点穿透和画中画等桌面端能力。",
            "封装基于 type 的消息/事件处理逻辑，提升多窗口状态同步和跨模块通信的可维护性。",
            "对接 TRTC 音视频能力，处理会议窗口、画面切换、订阅/取消订阅、状态同步等复杂交互。",
            "参与 Node 服务接口联调与部分业务接口开发，配合后端完成用户、权限、文件、会议状态等模块的数据链路打通。",
            "参与项目 Docker 镜像构建、环境变量配置、测试/生产环境部署与版本发布问题排查，协助处理容器日志和服务异常。",
            "实现本地工作目录与文件状态校验，支持文件目录动态匹配、生成、同步和异常状态处理。",
            "参与后台管理功能开发，覆盖人员、招聘、薪资、权限、系统配置等业务模块。",
        ],
    )

    add_project(
        doc,
        "项目周期待确认",
        "Node 服务与容器化部署实践",
        "Node.js / Express / Koa2 / Docker / Docker Compose / Kubernetes / Nginx / Git",
        "围绕业务系统前后端交付、接口服务、部署发布和环境维护开展的全栈工程化实践，重点支撑开发、测试、生产环境的一致性和可排查性。",
        [
            "参与 Node.js 服务开发，处理登录鉴权、基础数据查询、文件/资源代理、业务配置等接口场景，并完成前后端联调。",
            "根据不同环境维护接口地址、环境变量、构建参数和部署配置，降低开发、测试、生产环境差异导致的问题。",
            "编写或维护 Dockerfile / compose 配置，完成前端静态资源、Node 服务或相关依赖服务的容器化构建与启动。",
            "参与 Kubernetes 环境下的服务部署与运维协作，了解 Deployment、Service、ConfigMap、Secret、Ingress 等基础资源配置。",
            "配合排查线上/测试环境问题，通过容器日志、服务状态、接口响应、网络配置等维度定位发布失败、接口异常和环境配置问题。",
        ],
    )

    add_project(
        doc,
        "2021.04 - 2022.06",
        "MEUP 效率办公平台",
        "Vue / Electron / Element UI / Axios / Mock / ESLint / Prettier",
        "面向内部效率办公场景的平台，包含应用商城、工作台、知识库、广场、可视化平台等模块。",
        [
            "实现自定义 loading 指令，按页面接口请求状态展示加载反馈，优化弱网和多接口场景体验。",
            "开发全局可拖动标签、拖拽调整窗口区域、一键截图、应用图标读取等客户端交互能力。",
            "扩展富文本编辑器能力，支持自定义菜单和业务插件接入。",
            "参与安装包封装、应用安装状态识别和注册表读取等 Electron 桌面端能力建设。",
        ],
    )

    add_project(
        doc,
        "2020.03 - 2021.01",
        "应急指挥/可视化调度平台 [项目名待确认]",
        "Vue CLI / Electron / Cordova / ECharts / 地图 API / WebRTC / ESLint",
        "面向应急管理场景的信息化系统，包含管理平台与可视化调度平台，支持信息管理、组织架构、音视频会议、地图展示等能力。",
        [
            "参与可视化调度平台开发，对接多方数据与视频会议能力，支撑调度场景下的信息展示和协同沟通。",
            "基于 ECharts 和地图 API 完成数据可视化、区域分布、节点状态和功能布局展示。",
            "对接音视频 SDK / WebRTC 协议，实现多应用办公场景下的实时会议能力。",
            "参与后台管理平台建设，处理账号层级、权限分配、信息管理及可视化平台联动配置。",
        ],
    )

    add_project(
        doc,
        "2018.10 - 2020.05",
        "大屏播控系统",
        "Vue / ES6 / Sass / JavaScript / ESLint / Git",
        "面向本地播放器和大屏展示场景的播控系统，支持视频、图片、网页特效、节目编排和移动端控制。",
        [
            "负责大屏内容编排、播放区域拖拽定位、素材大小调整、嵌套多媒体内容展示等核心交互。",
            "通过网页嵌套与播放器能力结合，实现网页特效、视频可视化、账号管理等功能。",
            "参与手机端/平板端控制模块开发，通过 UDP 或接口指令实现场景切换、图片/视频上屏和播放状态控制。",
            "在多个项目场景中持续扩展和维护功能，提升系统稳定性与复用能力。",
        ],
    )

    add_heading(doc, "教育经历")
    add_body(doc, "2015.09 - 2018.06  |  湖南农业职业技术学院[待确认]  |  专业待确认  |  大专", size=9.5, after=2)

    doc.save(OUT)


if __name__ == "__main__":
    build()
    print(OUT)

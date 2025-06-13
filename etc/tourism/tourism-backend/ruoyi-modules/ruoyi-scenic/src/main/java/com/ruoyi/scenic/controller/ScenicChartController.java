package com.ruoyi.scenic.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.scenic.domain.Scenicareas;
import com.ruoyi.scenic.service.IScenicareasService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 景区信息Controller
 *
 * @author ningf
 * @date 2024-07-10
 */
@RestController
@RequestMapping("/scenicChart")
public class ScenicChartController extends BaseController
{
    @Autowired
    private IScenicareasService scenicareasService;

    /**
     * 查询景区信息列表
     */
    @RequiresPermissions("scenic:scenicChart:list")
    @GetMapping("/list")
    public TableDataInfo list(Scenicareas scenicareas)
    {
        startPage();
        List<Scenicareas> list = scenicareasService.selectScenicareasList(scenicareas);
        return getDataTable(list);
    }

    /**
     * 导出景区信息列表
     */
    @RequiresPermissions("scenic:scenicChart:export")
    @Log(title = "景区信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Scenicareas scenicareas)
    {
        List<Scenicareas> list = scenicareasService.selectScenicareasList(scenicareas);
        ExcelUtil<Scenicareas> util = new ExcelUtil<Scenicareas>(Scenicareas.class);
        util.exportExcel(response, list, "景区信息数据");
    }

    /**
     * 获取景区信息详细信息
     */
    @RequiresPermissions("scenic:scenicChart:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(scenicareasService.selectScenicareasById(id));
    }

    /**
     * 新增景区信息
     */
    @RequiresPermissions("scenic:scenicChart:add")
    @Log(title = "景区信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Scenicareas scenicareas)
    {
        return toAjax(scenicareasService.insertScenicareas(scenicareas));
    }

    /**
     * 修改景区信息
     */
    @RequiresPermissions("scenic:scenicChart:edit")
    @Log(title = "景区信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Scenicareas scenicareas)
    {
        return toAjax(scenicareasService.updateScenicareas(scenicareas));
    }

    /**
     * 删除景区信息
     */
    @RequiresPermissions("scenic:scenicChart:remove")
    @Log(title = "景区信息", businessType = BusinessType.DELETE)
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(scenicareasService.deleteScenicareasByIds(ids));
    }
}

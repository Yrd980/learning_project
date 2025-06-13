package com.ruoyi.entertainment.controller;

import java.util.List;
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
import com.ruoyi.entertainment.domain.Performancegroups;
import com.ruoyi.entertainment.service.IPerformancegroupsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 演出团体信息Controller
 * 
 * @author ningf
 * @date 2024-07-08
 */
@RestController
@RequestMapping("/performancegroups")
public class PerformancegroupsController extends BaseController
{
    @Autowired
    private IPerformancegroupsService performancegroupsService;

    /**
     * 查询演出团体信息列表
     */
    @RequiresPermissions("entertainment:performancegroups:list")
    @GetMapping("/list")
    public TableDataInfo list(Performancegroups performancegroups)
    {
        startPage();
        List<Performancegroups> list = performancegroupsService.selectPerformancegroupsList(performancegroups);
        return getDataTable(list);
    }

    /**
     * 导出演出团体信息列表
     */
    @RequiresPermissions("entertainment:performancegroups:export")
    @Log(title = "演出团体信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Performancegroups performancegroups)
    {
        List<Performancegroups> list = performancegroupsService.selectPerformancegroupsList(performancegroups);
        ExcelUtil<Performancegroups> util = new ExcelUtil<Performancegroups>(Performancegroups.class);
        util.exportExcel(response, list, "演出团体信息数据");
    }

    /**
     * 获取演出团体信息详细信息
     */
    @RequiresPermissions("entertainment:performancegroups:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(performancegroupsService.selectPerformancegroupsById(id));
    }

    /**
     * 新增演出团体信息
     */
    @RequiresPermissions("entertainment:performancegroups:add")
    @Log(title = "演出团体信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Performancegroups performancegroups)
    {
        return toAjax(performancegroupsService.insertPerformancegroups(performancegroups));
    }

    /**
     * 修改演出团体信息
     */
    @RequiresPermissions("entertainment:performancegroups:edit")
    @Log(title = "演出团体信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Performancegroups performancegroups)
    {
        return toAjax(performancegroupsService.updatePerformancegroups(performancegroups));
    }

    /**
     * 删除演出团体信息
     */
    @RequiresPermissions("entertainment:performancegroups:remove")
    @Log(title = "演出团体信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(performancegroupsService.deletePerformancegroupsByIds(ids));
    }
}

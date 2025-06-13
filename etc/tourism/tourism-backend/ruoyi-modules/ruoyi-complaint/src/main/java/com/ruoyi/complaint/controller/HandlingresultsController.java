package com.ruoyi.complaint.controller;

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
import com.ruoyi.complaint.domain.Handlingresults;
import com.ruoyi.complaint.service.IHandlingresultsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 投诉处理结果Controller
 * 
 * @author ningf
 * @date 2024-07-15
 */
@RestController
@RequestMapping("/handlingresults")
public class HandlingresultsController extends BaseController
{
    @Autowired
    private IHandlingresultsService handlingresultsService;

    /**
     * 查询投诉处理结果列表
     */
    @RequiresPermissions("complaint:handlingresults:list")
    @GetMapping("/list")
    public TableDataInfo list(Handlingresults handlingresults)
    {
        startPage();
        List<Handlingresults> list = handlingresultsService.selectHandlingresultsList(handlingresults);
        return getDataTable(list);
    }

    /**
     * 导出投诉处理结果列表
     */
    @RequiresPermissions("complaint:handlingresults:export")
    @Log(title = "投诉处理结果", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Handlingresults handlingresults)
    {
        List<Handlingresults> list = handlingresultsService.selectHandlingresultsList(handlingresults);
        ExcelUtil<Handlingresults> util = new ExcelUtil<Handlingresults>(Handlingresults.class);
        util.exportExcel(response, list, "投诉处理结果数据");
    }

    /**
     * 获取投诉处理结果详细信息
     */
    @RequiresPermissions("complaint:handlingresults:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(handlingresultsService.selectHandlingresultsById(id));
    }

    /**
     * 新增投诉处理结果
     */
    @RequiresPermissions("complaint:handlingresults:add")
    @Log(title = "投诉处理结果", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Handlingresults handlingresults)
    {
        return toAjax(handlingresultsService.insertHandlingresults(handlingresults));
    }

    /**
     * 修改投诉处理结果
     */
    @RequiresPermissions("complaint:handlingresults:edit")
    @Log(title = "投诉处理结果", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Handlingresults handlingresults)
    {
        return toAjax(handlingresultsService.updateHandlingresults(handlingresults));
    }

    /**
     * 删除投诉处理结果
     */
    @RequiresPermissions("complaint:handlingresults:remove")
    @Log(title = "投诉处理结果", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(handlingresultsService.deleteHandlingresultsByIds(ids));
    }
}
